from django.conf import settings
from django.db import models

class Transaction(models.Model):
    STATUS_CHOICES = (('Pending', 'Pending'),('Paid', 'Paid'))
    
    customer = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)  # type: ignore
    product = models.ForeignKey('stock.Gas', on_delete=models.CASCADE, related_name='transaction' )
    status = models.CharField(max_length=32, default="Pending", choices = STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return f"{self.quantity} - {self.product.price}"
    
    def total_cost(self):
        try:
            return self.quantity * self.product.price
        except Exception as e:
            settings.LOGGER.error(e)
            return 0.00

    def get_order_number(self):
        return self.created.strftime('%s')[2:7]