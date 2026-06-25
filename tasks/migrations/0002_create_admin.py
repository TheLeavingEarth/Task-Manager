from django.db import migrations
import os

def create_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    email = os.getenv("ADMIN_EMAIL")

    if not username or not password:
        return  # ничего не делаем, если нет переменных

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            password=password,
            email=email
        )

def reverse_func(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    username = os.getenv("ADMIN_USERNAME")
    if username:
        User.objects.filter(username=username).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin, reverse_func),
    ]