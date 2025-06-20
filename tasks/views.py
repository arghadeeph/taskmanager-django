from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Task
from django.contrib import messages
from django.utils import timezone

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def register(request):
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if not all([first_name, last_name, email, password, confirm_password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html', {'first_name': first_name, 'last_name': last_name, 'email': email})

        if password != confirm_password:
            messages.error(request, 'Password & Confirm Password must match!')
            return render(request, 'register.html', {'first_name': first_name, 'last_name': last_name, 'email': email})
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'register.html', {'first_name': first_name, 'last_name': last_name})

        user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=email, password=password)
        login(request, user)
        return redirect('/')
    
    return render(request, 'register.html')

@login_required
def index(request):
    tasks = Task.objects.filter(user = request.user).order_by('-created_at')
    if tasks :
        for task in tasks:
            if task.completed :
                task.formatted_completed = task.completed.strftime('%d %b, %Y %H:%M')
            task.formatted_created = task.created_at.strftime('%d %b, %Y %H:%M')
    return render(request, 'index.html', {'tasks' : tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']

        task = Task.objects.create(title = title, details=description, user=request.user)
        return redirect('task-list')
    return render(request, 'task-form.html')

@login_required
def complete_task(request, task_id:int):
    task = Task.objects.filter(id=task_id).first()
    task.completed = timezone.now()
    task.save()
    messages.success(request, 'Task Completed Successfully!')
    return redirect('/')

@login_required
def delete_task(request, task_id:int):
    task = Task.objects.filter(id=task_id).first().delete()
    messages.success(request, 'Task Deleted Successfully!')
    return redirect('/')