# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet)

urlpatterns = [
    path('ind-task/',views.get_and_update_task,name="get or update individual task"),
    path('task-list/', views.TaskList.as_view(), name='task list'),
    path('', include(router.urls)),
]