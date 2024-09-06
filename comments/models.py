from django.db import models
from users.models import CustomUser
from tasks.models import Task

class Comment(models.Model):
    comment=models.TextField(max_length=300)
    owner=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    task_id=models.ForeignKey(Task,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.comment