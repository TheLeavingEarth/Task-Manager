from django.urls import path
from . import views

urlpatterns = [
	path('', views.task_list, name='list'),
	path('add/', views.add_task, name='add'),
	path('delete/<int:id>/', views.delete_task, name='delete'),
	path('status/<int:id>/<str:status>/', views.change_status, name='change_status'),
	path('edit/<int:id>/', views.edit_task, name='edit'),
]