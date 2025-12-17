from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Success", "Success"),
        ("Failed", "Failed"),
    ]
    
    # Link transaction to a user (optional)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Customer details
    name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=12,
        help_text="Phone number in format 2547XXXXXXXX"
    )
    
    # Payment details
    amount = models.PositiveIntegerField()
    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Daraja CheckoutRequestID from Mpesa"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # optional: latest transactions first

    def __str__(self):
        return f"{self.name} - {self.status} - {self.amount}"
