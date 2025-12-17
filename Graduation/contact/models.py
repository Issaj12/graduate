from django.db import models

# create ypur models here
class Contact(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True)  # Optional field
    message = models.TextField()

    def __str__(self):
        return self.name