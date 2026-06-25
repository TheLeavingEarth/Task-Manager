from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.task_list, name='list'),

    path('add/', views.add_task, name='add'),
    path('edit/<int:id>/', views.edit_task, name='edit'),
    path('delete/<int:id>/', views.delete_task, name='delete'),
    path('change-status/<int:id>/<str:status>/', views.change_status, name='change_status'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]