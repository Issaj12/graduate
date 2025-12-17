from django import forms
from .models import Transaction

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['name', 'phone_number', 'amount']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['name'].initial = user.get_full_name() or user.username
