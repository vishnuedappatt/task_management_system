from django.urls import path

from users import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<int:user_id>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('userlist/',views.UserList.as_view(),name="user list")
]