# Generated by Django 3.2.5 on 2021-07-24 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webproject', '0006_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
