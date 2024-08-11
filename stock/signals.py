from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Stock

@receiver(post_save, sender=Stock)
def send_stock_alert(sender, instance, **kwargs):
    if instance.quantity < instance.minimum_threshold:
        subject = f"Stock stock alert: {instance.name}"
        message = f"The stock of {instance.name} is below {instance.minimum_threshold} units."
        from_email = "noreply@egds.com"
        recipient_list = ["nchizampeni@gmail.com"]
        send_mail(subject, message, from_email, recipient_list)