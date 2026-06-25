from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.decorators import login_required

# Список задач
@login_required
def task_list(request):
    query = request.GET.get('q')
    status = request.GET.get('status')

    tasks = Task.objects.filter(user=request.user)

    # Поиск
    if query:
        tasks = tasks.filter(title__icontains=query)

    # Фильтр
    if status:
        tasks = tasks.filter(status=status)

    # Статистика
    total = tasks.count()
    in_progress = tasks.filter(status='progress').count()
    completed = tasks.filter(status='done').count()

    return render(request, 'tasks/list.html', {
        'tasks': tasks,
        'total': total,
        'in_progress': in_progress,
        'completed': completed,
    })


# Добавление
@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status', 'new')
        assignee = request.POST.get('assignee')

        if title:
            Task.objects.create(
                title=title,
                status=status,
                assignee=assignee,
                user=request.user
            )

    return redirect('list')


# Удаление
@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()
    return redirect('list')


# Смена статуса
@login_required
def change_status(request, id, status):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.status = status
    task.save()
    return redirect('list')


# Редактирование
@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status')
        assignee = request.POST.get('assignee')

        if title:
            task.title = title
            task.status = status
            task.assignee = assignee
            task.save()

    return redirect('list')