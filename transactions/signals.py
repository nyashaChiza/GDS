from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction

@receiver(post_save, sender=Transaction)
def reduce_stock_quantity(sender, instance, created, **kwargs):
    if created:  # New transaction
        instance.product.quantity -= instance.quantity
        instance.product.save()
    else:  # Existing transaction
        original_transaction = Transaction.objects.get(pk=instance.pk)
        quantity_diff = instance.quantity - original_transaction.quantity
        instance.product.quantity -= quantity_diff
        instance.product.save()