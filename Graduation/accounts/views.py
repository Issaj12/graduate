from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.views import PasswordResetView
from .forms import CustomPasswordResetForm
from django.contrib.auth.views import LogoutView

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect("login")
    else:
         form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "account/register.html", context)


class CustomPasswordResetView(PasswordResetView):
    template_name = "account/password_reset.html"
    form_class = CustomPasswordResetForm
    success_url = "/accounts/password_reset_done/" 


class CustomLogoutView(LogoutView):
    next_page = 'login'  # Redirect to login page after logout

    # Treat GET as POST
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
 
