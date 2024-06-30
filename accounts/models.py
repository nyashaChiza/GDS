from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import Group
from django.db.models import Q



class Site(models.Model):
    STATUS_CHOICES = (('Active', 'Active'), ('Disabled', 'Disabled'))
    name = models.CharField(max_length=255)
    address = models.TextField()
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    operator = models.ForeignKey('accounts.User', blank=True, null=True, on_delete=models.SET_NULL, related_name='sites')
    manager = models.OneToOneField('accounts.User', blank=True, null=True, on_delete=models.SET_NULL, related_name='site')

    def __str__(self) -> str:
        return f"{self.name}"

