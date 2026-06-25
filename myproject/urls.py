from django.contrib import admin
from django.urls import path, include

print("MAIN URLS LOADED")

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),  #  подключаем приложение
    path('accounts/', include('django.contrib.auth.urls')),
]


