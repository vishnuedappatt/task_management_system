# Generated by Django 4.2.15 on 2024-09-06 06:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('priority', models.CharField(choices=[('HIGH', 'HIGH'), ('MEDIUM', 'MEDIUM'), ('LOW', 'LOW')], default='MEDIUM', max_length=20)),
                ('due_date', models.DateField()),
                ('status', models.CharField(choices=[('TODO', 'todo'), ('IN-PROGRESS', 'in-progress'), ('DONE', 'done')], default='todo')),
                ('type', models.CharField(choices=[('PUBLIC', 'public'), ('PRIVATE', 'private')], default='public')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
