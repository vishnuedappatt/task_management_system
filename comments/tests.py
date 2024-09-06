from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Comment
from users.models import CustomUser
from tasks.models import Task

class CommentViewTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='user1@example.com', password='userpassword')
        self.client.force_authenticate(user=self.user)
        self.create_comment_url = reverse('comment add')
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(
            name="Sample Task", 
            type="PUBLIC", 
            owner=self.user,
            due_date='2024-09-30'
        )


    def test_create_comment(self):
        data =  {
            "comment": "comment addded",
            "task_id":self.task.id,
            "owner":self.user.id
        }
        response = self.client.post(self.create_comment_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 1)
       

    def test_create_comment_invalid(self):
        data = {"text": ""}
        response = self.client.post(self.create_comment_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class CommentRetrieveUpdateViewTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='user@example.com', password='userpassword')
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(
            name="Sample Task", 
            type="PUBLIC", 
            owner=self.user,
            due_date='2024-09-30'
        )
        self.comment = Comment.objects.create(
            comment="Initial comment text.",
            owner=self.user,
            task_id=self.task
        )
        self.retrieve_update_comment_url = reverse('task-retrieve-update', kwargs={'id': self.comment.id})

    def test_retrieve_comment(self):
        response = self.client.get(self.retrieve_update_comment_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
     

    def test_update_comment(self):
        data = {"comment": "Updated comment text.", "owner":self.user.pk,"task_id":self.task.pk}
        response = self.client.put(self.retrieve_update_comment_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['comment'], "Updated comment text.")
        self.comment.refresh_from_db()
      

    def test_update_comment_invalid(self):
        data = {"text": ""}
        response = self.client.put(self.retrieve_update_comment_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)