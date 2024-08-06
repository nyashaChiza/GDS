import uuid
from django.conf import settings
from django.db import models

class Transaction(models.Model):
    STATUS_CHOICES = (('Pending', 'Pending'), ('Paid', 'Paid'))
    
    site = models.ForeignKey('accounts.Site', on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)  # type: ignore
    product = models.ForeignKey('stock.Gas', on_delete=models.CASCADE, related_name='transaction')
    status = models.CharField(max_length=32, default="Pending", choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order_number = models.CharField(max_length=36, unique=True, blank=True, editable=False)

    def __str__(self):
        return f"{self.quantity} - {self.product.price}"

    def total_cost(self):
        try:
            return self.quantity * self.product.price
        except Exception as e:
            settings.LOGGER.error(e)
            return 0.00

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        # Generate a random UUID
        order_uuid = uuid.uuid4()
        return f"#{order_uuid.hex[:8]}".upper()
