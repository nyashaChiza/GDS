from random import choices
from django.db import models
import uuid
from django.urls import reverse
from payments import PurchasedItem
from payments.models import BasePayment


STATUS_CHOICES = (('Active', 'Active'), ('Suspended', 'Suspended'))

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price_per_site = models.DecimalField(max_digits=10, decimal_places=2)
    max_sites = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

class BillingProfile(models.Model):
    class Meta:
            indexes = [
            models.Index(fields=['company']),
            models.Index(fields=['subscription_status']),
        ]
    admin = models.OneToOneField('accounts.User', null=True, blank=True, on_delete=models.SET_NULL, )
    company = models.ForeignKey('accounts.Company', on_delete=models.CASCADE, related_name='bill_profiles')
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    subscription_status = models.CharField(max_length=50, default='Active', choices=STATUS_CHOICES)
    last_payment_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def calculate_total_due(self):
        total_sites = self. company.site_count()
        total_due = total_sites * self.subscription_plan.price_per_site
        return total_due

    def __str__(self):
        return f"{self.company.name} - {self.subscription_plan.name}"

class Invoice(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('ZWL', 'Zimbabwean Dollar'),       # Zimbabwe
        ('ZAR', 'South African Rand'),      # South Africa
        ('BWP', 'Botswana Pula'),           # Botswana
        ('NAD', 'Namibian Dollar'),         # Namibia
        ('MWK', 'Malawian Kwacha'),         # Malawi
        ('ZMW', 'Zambian Kwacha'),          # Zambia
        ('MZN', 'Mozambican Metical'),      # Mozambique
        ('SZL', 'Swazi Lilangeni'),         # Eswatini (Swaziland)
        ('LSL', 'Lesotho Loti'),            # Lesotho
        
    ]
    STATUS_CHOICES = [('Pending', 'Pending'), ('Paid', 'Paid'), ('Overdue', 'Overdue')]
    
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    billing_profile = models.ForeignKey('BillingProfile', on_delete=models.CASCADE)
    date_issued = models.DateField(auto_now_add=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    currency = models.CharField(max_length=255, choices=CURRENCY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_date = models.DateField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_amount(self):
        return self.amount_due

    def get_currency(self):
        return self.currency

    def save(self, *args, **kwargs):
        if not self.amount_due:
            self.amount_due = self.billing_profile.calculate_total_due()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.pk} for {self.billing_profile.company.name}"


class Payment(BasePayment):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    PAYMENT_CHOICES = [('Card', 'Card'), ('Bank Transfer', 'Bank Transfer'), ('Mobile Money', 'Mobile Money')]
    invoice = models.ForeignKey(Invoice, related_name='payments', on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_failure_url(self):
        return reverse('payment_failed')

    def get_success_url(self):
        return reverse('payment_success')

    def get_purchased_items(self):
        yield PurchasedItem(
            name=f"Invoice {self.invoice.uuid}",
            quantity=self.invoice.billing_profile.company.site_count(),
            price=self.invoice.get_amount(),
            currency=self.invoice.get_currency(),
            sku=f"invoice-{self.invoice.uuid}"
        )

