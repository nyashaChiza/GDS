from django.db import models
from django.contrib.auth.models import User 


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    site = models.ForeignKey('accounts.Site', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    organisation = models.OneToOneField('accounts.Organisation', on_delete=models.CASCADE, related_name="users")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)