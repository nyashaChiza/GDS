from django.db import models

class Organisation(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}"