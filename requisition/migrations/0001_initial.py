# Generated by Django 5.0 on 2024-08-18 04:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requisition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requisition_type', models.CharField(choices=[('Stock', 'Stock'), ('Equipment', 'Equipment'), ('Other', 'Other')], max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied'), ('Delivered', 'Delivered')], max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.site')),
            ],
            options={
                'indexes': [models.Index(fields=['site'], name='requisition_site_id_a3906d_idx'), models.Index(fields=['requisition_type'], name='requisition_requisi_8fc3eb_idx'), models.Index(fields=['status'], name='requisition_status_9967f2_idx'), models.Index(fields=['created'], name='requisition_created_1cfd2a_idx'), models.Index(fields=['updated'], name='requisition_updated_a3f600_idx')],
            },
        ),
    ]
