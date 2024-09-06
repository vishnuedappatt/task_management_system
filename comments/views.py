from .serializers import CommentSerializer
from users.permissions import IsStandardUser,IsAdminUser
from rest_framework.response import Response
from rest_framework import status,views,generics
from .models import Comment

class CommentView(views.APIView):
    permission_classes = [IsStandardUser]
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """View to retrieve (GET) and update (PUT) a comment."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'  

    def put(self, request, *args, **kwargs):
        """Handle PUT request for full update."""
        return self.update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Handle GET request to retrieve a comment."""
        return self.retrieve(request, *args, **kwargs)
    


