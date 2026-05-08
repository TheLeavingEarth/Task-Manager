from django.shortcuts import render, redirect, get_object_or_404
from .models import Task


def task_list(request):
    query = request.GET.get('q')
    status = request.GET.get('status')

    tasks = Task.objects.all()

    # 🔍 Поиск
    if query:
        tasks = tasks.filter(title__icontains=query)

    # 📊 Фильтр
    if status:
        tasks = tasks.filter(status=status)

    # 📊 СТАТИСТИКА
    total = tasks.count()
    in_progress = tasks.filter(status='progress').count()
    completed = tasks.filter(status='done').count()

    return render(request, 'tasks/list.html', {
        'tasks': tasks,
        'total': total,
        'in_progress': in_progress,
        'completed': completed,
    })


# ➕ Добавление
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status', 'new')
        assignee = request.POST.get('assignee')  # 👈 НОВОЕ

        if title:
            Task.objects.create(
                title=title,
                status=status,
                assignee=assignee
            )

    return redirect('list')


# ❌ Удаление
def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()
    return redirect('list')


# 🔄 Смена статуса
def change_status(request, id, status):
    task = get_object_or_404(Task, id=id)
    task.status = status
    task.save()
    return redirect('list')


# ✏ Редактирование
def edit_task(request, id):
    task = get_object_or_404(Task, id=id)

    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status')
        assignee = request.POST.get('assignee')  # 👈 НОВОЕ

        if title:
            task.title = title
            task.status = status
            task.assignee = assignee  # 👈 НОВОЕ
            task.save()

    return redirect('list')