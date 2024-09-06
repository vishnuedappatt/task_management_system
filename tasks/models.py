from django.db import models
from users.models import CustomUser

PRIORITY = (
        ("HIGH", "HIGH"),
        ("MEDIUM", "MEDIUM"),
        ("LOW", "LOW")
)
STATUS=(
    ("TODO","todo"),
    ("IN-PROGRESS","in-progress"),
    ("DONE","done")
)

TYPES=(
    ("PUBLIC","public"),
    ("PRIVATE","private")
)
class Task(models.Model):
    name=models.CharField(max_length=30,blank=False,null=False)
    description=models.TextField(max_length=200,blank=True,null=True)
    priority=models.CharField(max_length=20,choices=PRIORITY,default='MEDIUM')
    owner=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    due_date=models.DateField()
    status=models.CharField(choices=STATUS,default='todo')
    type=models.CharField(choices=TYPES,default='public')
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name