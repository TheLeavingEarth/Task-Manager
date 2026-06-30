import datetime
from django.db.models import Value, DateField
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Task
from django.contrib.auth.decorators import login_required


@login_required
def task_list(request):
    query = request.GET.get('q')
    status = request.GET.get('status')

    tasks = Task.objects.filter(user=request.user)
    if query:
        tasks = tasks.filter(title__icontains=query)
    if status:
        tasks = tasks.filter(status=status)

    total = tasks.count()
    in_progress = tasks.filter(status='progress').count()
    completed = tasks.filter(status='done').count()

    # Активные — сортировка по сроку (без срока — в конец списка)
    active_tasks = (
        tasks.exclude(status='done')
        .annotate(sort_deadline=Coalesce('deadline', Value(datetime.date.max, output_field=DateField())))
        .order_by('sort_deadline')
    )

    # Завершённые — сортировка по дате завершения (если её нет у старых записей — по дате создания)
    completed_tasks = (
        tasks.filter(status='done')
        .annotate(sort_completed=Coalesce('completed_at', 'created_at'))
        .order_by('-sort_completed')
    )

    return render(request, 'tasks/list.html', {
        'active_tasks': active_tasks,
        'completed_tasks': completed_tasks,
        'total': total,
        'in_progress': in_progress,
        'completed': completed,
        'today': timezone.now().date(),
        'has_filters': bool(query or status),
    })


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status', 'new')
        assignee = request.POST.get('assignee')
        deadline = request.POST.get('deadline') or None

        if title:
            Task.objects.create(
                title=title, status=status, assignee=assignee,
                deadline=deadline, user=request.user
            )
            messages.success(request, f'Задача «{title}» создана')
    return redirect('list')


@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    title = task.title
    task.delete()
    messages.success(request, f'Задача «{title}» удалена')
    return redirect('list')


@login_required
def change_status(request, id, status):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.status = status
    if status == 'done' and not task.completed_at:
        task.completed_at = timezone.now()
    elif status != 'done':
        task.completed_at = None
    task.save()
    messages.success(request, f'Статус задачи «{task.title}» изменён на «{task.get_status_display()}»')
    return redirect('list')


@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status')
        assignee = request.POST.get('assignee')
        deadline = request.POST.get('deadline') or None

        if title:
            if status == 'done' and task.status != 'done':
                task.completed_at = timezone.now()
            elif status != 'done':
                task.completed_at = None
            task.title = title
            task.status = status
            task.assignee = assignee
            task.deadline = deadline
            task.save()
            messages.success(request, f'Задача «{title}» обновлена')
    return redirect('list')