# Generated by Django 3.2.9 on 2024-03-05 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20240305_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='payment_check',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
