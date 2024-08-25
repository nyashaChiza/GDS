from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid

ROLES = (('Admin', 'Admin'), ('Manager', 'Manager'), ('Operator', 'Operator'))
GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
STATUS_CHOICES = (('Active', 'Active'), ('Suspended', 'Suspended'),('Draft', 'Draft'))

class Company(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
    
    def site_count():
        return self.sites.filter(status="Active").count()
    
    
class Site(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    address = models.TextField()
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Suspended')
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, blank=True, null=True, related_name='sites')
    contact = models.CharField(max_length=255)
    capacity = models.FloatField(default=0.00)
    operator = models.OneToOneField('User', on_delete=models.SET_NULL, blank=True, null=True, related_name='operation_site')
    manager = models.OneToOneField('User', on_delete=models.SET_NULL, blank=True, null=True, related_name='managed_site')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"

class User(AbstractUser):
    role = models.CharField(max_length=255, choices=ROLES)
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    is_logged_in = models.BooleanField(default=False)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, blank=True, null=True, related_name='users')
    display_picture = models.ImageField(upload_to='display_images/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def avatar(self):
        try:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        except Exception as e:
            settings.LOGGER.error(e)
            return f"{self.role[0:2]}".upper()
