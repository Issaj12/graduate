from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomPasswordResetView  # <--- ADD THIS LINE

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="account/login.html"), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),

    # Password reset URLs
    path("password_reset/", 
         CustomPasswordResetView.as_view(),  # Use the imported view
         name="password_reset"),
    path("password_reset_done/", 
         auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"), 
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html"), 
         name="password_reset_confirm"),
    path("reset/done/", 
         auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"), 
         name="password_reset_complete"),
]
