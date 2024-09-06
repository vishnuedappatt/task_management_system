from django.urls import path

from comments import views

urlpatterns = [
        path('add-comment/', views.CommentView.as_view(), name='comment add'),
        path('get-or-update-comment/<int:id>/',views.CommentRetrieveUpdateView.as_view(),name='task-retrieve-update'),
]