from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid

ROLES = (('Admin', 'Admin'), ('Manager', 'Manager'), ('Operator', 'Operator'))
GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
STATUS_CHOICES = (('Active', 'Active'), ('Suspended', 'Suspended'))

class Site(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    address = models.TextField()
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    contact = models.CharField(max_length=255)
    capacity = models.FloatField(default=0.00)
    manager = models.OneToOneField('User', on_delete=models.SET_NULL, blank=True, null=True, related_name='managed_site')

    def __str__(self) -> str:
        return f"{self.name}"

class User(AbstractUser):
    role = models.CharField(max_length=255, choices=ROLES)
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    is_logged_in = models.BooleanField(default=False)
    email = models.EmailField(max_length=255)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    display_picture = models.ImageField(upload_to='display_images/', null=True, blank=True)
    site = models.OneToOneField(Site, blank=True, on_delete=models.SET_NULL, null=True, related_name='operator')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
