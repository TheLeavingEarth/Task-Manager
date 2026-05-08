from django.db import models

class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('progress', 'В работе'),
        ('done', 'Завершена'),
    ]

    title = models.CharField(max_length=200)
    assignee = models.CharField(max_length=100, blank=True)  #  имя
    created_at = models.DateTimeField(auto_now_add=True)     #  время
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return self.title