from rest_framework import permissions, status, views,generics
from rest_framework.response import Response
from users.models import CustomUser
from users.serializers import UserSignupSerializer, LoginSerializer,UserSerializer
from django.core.mail import send_mail
from django.urls import reverse
from users.permissions import IsAdminUser
from rest_framework import filters

class SignupView(views.APIView):
    """Sign Up"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            html=f"""
            Hi! {serializer.data["name"]}  \n
            Welcome to our Task Management System \n
            Explore The features inside us!!!
            """
            send_mail("WELCOME TO OUR TASK MANAGEMENT SYSTEM",html, 'from taskmanager.com',[serializer.data["email"]])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    """Login"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = serializer.get_tokens(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PasswordResetView(views.APIView):
    """ reset password email trigger """
    def post(self, request):
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            reset_url = request.build_absolute_uri(reverse('password_reset_confirm', args=[user.id]))
            send_mail(
                'Password Reset',
                f'Click the link to reset your password: {reset_url}',
                'from taskmanager.com',
                [email],
                fail_silently=False,
            )
            return Response({'detail': 'Password reset email sent.'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'No user found with the provided email.'}, status=status.HTTP_404_NOT_FOUND)
        


class PasswordResetConfirmView(views.APIView):
    """ password reset """
    def post(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        new_password = request.data.get('new_password')
        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Password reset successfully.'}, status=status.HTTP_200_OK)


class UserList(generics.ListAPIView):
    """ view userlist """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter] 
    search_fields = ['name', 'email'] 