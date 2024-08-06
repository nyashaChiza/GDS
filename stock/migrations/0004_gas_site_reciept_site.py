# Generated by Django 5.0 on 2024-08-06 21:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('stock', '0003_reciept'),
    ]

    operations = [
        migrations.AddField(
            model_name='gas',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.site'),
        ),
        migrations.AddField(
            model_name='reciept',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.site'),
        ),
    ]
