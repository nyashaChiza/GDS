from django.db import models

class Site(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    capacity = models.FloatField(null=True, blank=True)
    organisation = models.ForeignKey('accounts.Organisation', on_delete=models.RESTRICT, related_name='sites')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}"