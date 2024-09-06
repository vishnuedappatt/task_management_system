from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import api_view
from users.permissions import IsStandardUser,IsAdminUser
from rest_framework.response import Response
from rest_framework import status,viewsets,generics
from django.db.models import Q

class TaskViewSet(viewsets.ModelViewSet):
    """ creating ,deleting ,updating and viewing task by admin """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdminUser]




@api_view(['GET', 'PUT'])
def get_and_update_task(request):
    """Get all tasks assigned to the user and update the task details."""
    permission = IsStandardUser()
    if not permission.has_permission(request, None):
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
    task_id = request.query_params.get('id', None)

    if task_id is None:
        return Response({"detail": "task_id parameter is mandatory"})
    if request.method == "PUT":
        try:
            task = Task.objects.get(id=task_id, owner=request.user)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data, partial=True) 

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else: 
        try:
            tasks = Task.objects.get(id=task_id, owner=request.user)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(tasks, many=False)
        return Response(serializer.data)
    


class TaskList(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes=[IsStandardUser]
    def get_queryset(self):
        
        task_type = self.request.query_params.get('type', None)
        name_keyword = self.request.query_params.get('name', None) 

        queryset = Task.objects.all()

        if task_type:
            queryset = queryset.filter(type=task_type)
        else:
            queryset = queryset.filter(type="PRIVATE")
        
        if name_keyword:
            queryset = queryset.filter(name__icontains=name_keyword)
        
        return queryset
      