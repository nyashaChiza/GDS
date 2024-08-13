import uuid
from django.db import models

class Requisition(models.Model):
    STATUS_CHOICES = (('Pending', 'Pending'),('Approved', 'Approved'), ('Denied', 'Denied'),('Delivered', 'Delivered'))
    REQUISITION_TYPES = (('Stock','Stock'), ('Equipment', 'Equipment'), ('Other', 'Other'))
    site = models.ForeignKey('accounts.Site', on_delete=models.SET_NULL, null=True, blank=True)
    requisition_type = models.CharField(max_length=255, choices=REQUISITION_TYPES)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return f"{self.requisition_type}"
    
    class Meta:
        indexes = [
            models.Index(fields=['site']),
            models.Index(fields=['requisition_type']),
            models.Index(fields=['status']),
            models.Index(fields=['created']),
            models.Index(fields=['updated']),
        ]