from django.db import models

class Image(models.Model):
    photo = models.ImageField(upload_to='images/') 
    description = models.TextField(blank=True, null=True)  
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description[:20]}"
