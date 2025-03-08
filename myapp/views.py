from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse  # For sending JSON responses
from django.views.decorators.csrf import csrf_exempt  # To allow AJAX requests without CSRF issues

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Task
from .forms import TaskForm, RegisterForm
from datetime import timedelta, date

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')
    return render(request, 'login.html')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST.get("description", "")
        due_date = request.POST["due_date"]
        hours = request.POST["hours"]

        Task.objects.create(user=request.user, title=title, description=description, due_date=due_date, hours=hours)
        return redirect("task_list")

    return render(request, "myapp/add_task.html")

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        task.title = request.POST["title"]
        task.description = request.POST.get("description", "")
        task.due_date = request.POST["due_date"]

        # Don't update hours if already set
        if task.hours is None:
            task.hours = request.POST["hours"]

        task.save()
        return redirect("task_list")

    return render(request, "myapp/edit_task.html", {"task": task})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    return render(request, 'task_detail.html', {'task': task})



@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'delete_task.html', {'task': task})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return redirect('task_list')

@login_required
def weekly_report(request):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    weekly_tasks = Task.objects.filter(user=request.user, due_date__range=[start_of_week, end_of_week])
    return render(request, 'myapp/weekly_report.html', {'tasks': weekly_tasks})

@login_required
def monthly_report(request):
    today = date.today()
    start_of_month = today.replace(day=1)
    if today.month == 12:
        end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)

    monthly_tasks = Task.objects.filter(user=request.user, due_date__range=[start_of_month, end_of_month])
    return render(request, 'myapp/monthly_report.html', {'tasks': monthly_tasks})

@csrf_exempt
def toggle_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed  # Toggle status
    task.save()
    
    return JsonResponse({'status': "Completed" if task.completed else "Not Completed"})