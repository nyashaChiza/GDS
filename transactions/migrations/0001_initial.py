# Generated by Django 5.0 on 2024-08-18 04:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit_cost', models.DecimalField(decimal_places=2, default=1.0, max_digits=10)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('order_number', models.CharField(blank=True, editable=False, max_length=36, unique=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='stock.stock')),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.site')),
            ],
            options={
                'indexes': [models.Index(fields=['site'], name='transaction_site_id_5650b6_idx'), models.Index(fields=['customer'], name='transaction_custome_d6a353_idx'), models.Index(fields=['product'], name='transaction_product_f7931b_idx'), models.Index(fields=['status'], name='transaction_status_71abbb_idx'), models.Index(fields=['created'], name='transaction_created_93d56d_idx'), models.Index(fields=['updated'], name='transaction_updated_4accb6_idx')],
            },
        ),
    ]
