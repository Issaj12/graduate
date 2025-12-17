from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
    }))

    agree_to_family_use = forms.BooleanField(
        required=True,
        label="I agree that the information I provide will be used by family only."
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'agree_to_family_use')


class CustomPasswordResetForm(PasswordResetForm):
    username = forms.CharField(max_length=150, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        if username and email:
            try:
                User.objects.get(username=username, email=email, is_active=True)
            except User.DoesNotExist:
                raise forms.ValidationError(
                    "No user found with this username and email combination."
                )
        return cleaned_data

    # Override get_users so only the correct user gets the email
    def get_users(self, email):
        username = self.cleaned_data.get("username")
        try:
            user = User.objects.get(username=username, email=email, is_active=True)
            return [user]
        except User.DoesNotExist:
            return []
