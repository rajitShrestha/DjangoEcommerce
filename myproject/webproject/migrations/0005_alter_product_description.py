# Generated by Django 3.2.5 on 2021-07-19 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webproject', '0004_auto_20210718_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]