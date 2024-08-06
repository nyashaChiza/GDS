# Generated by Django 5.0 on 2024-08-06 21:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('transactions', '0006_transaction_order_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.site'),
        ),
    ]
