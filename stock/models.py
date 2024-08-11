from django.db import models


class Stock(models.Model):
    name = models.CharField(max_length=100)
    site = models.ForeignKey('accounts.Site', on_delete=models.SET_NULL, null=True, blank=True, related_name='stock')
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    supplier = models.CharField(max_length=100, null=True, blank=True)
    minimum_threshold = models.PositiveIntegerField(default= 50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
    
class Reciept(models.Model):
    site = models.ForeignKey('accounts.Site', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    stock = models.ForeignKey(Stock, related_name='reciepts', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.stock} - {self.quantity}"
