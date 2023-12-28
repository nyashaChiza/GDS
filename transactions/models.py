from django.db import models

class Transaction(models.Model):
    customer = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey('stock.Gas', on_delete=models.CASCADE, related_name='transaction' )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return f"{self.quantity} - {self.product.price}"
    
    def total_cost(self):
        try:
            return self.quantity * self.product.price
        except Exception as e:
            return 0.00
