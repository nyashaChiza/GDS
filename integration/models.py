from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings
from django.forms import ValidationError
from simple_history.models import HistoricalRecords

class Integration(models.Model):
    integration_id = models.CharField(max_length=255)
    integration_key = models.CharField(max_length=255)
    result_url = models.URLField(max_length=255)
    return_url = models.URLField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()  # Add history tracking
    
    cipher_suite = Fernet(settings.FERNET_KEY.encode())

    def save(self, *args, **kwargs):
        # Encrypt only sensitive data if it's not already encrypted
        if not self.is_encrypted(self.integration_id):
            self.integration_id = self.encrypt_data(self.integration_id)
        if not self.is_encrypted(self.integration_key):
            self.integration_key = self.encrypt_data(self.integration_key)
        super().save(*args, **kwargs)

    def encrypt_data(self, data):
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return encrypted_data.decode()

    def decrypt_data(self, encrypted_data):
        decrypted_data = self.cipher_suite.decrypt(encrypted_data.encode())
        return decrypted_data.decode()

    def is_encrypted(self, data):
        # Check if the data appears to be encrypted
        try:
            self.cipher_suite.decrypt(data.encode())
            return True
        except:
            return False

    def clean(self):
        # This method will validate the plain URL fields without decrypting
        try:
            models.URLField().clean(self.result_url, self)
            models.URLField().clean(self.return_url, self)
        except ValidationError as e:
            raise ValidationError(f"Invalid URL format: {e}")

    def __str__(self):
        return "Payment Gateway Integration"
