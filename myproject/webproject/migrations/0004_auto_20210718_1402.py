# Generated by Django 3.2.5 on 2021-07-18 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webproject', '0003_auto_20210718_1357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='tag',
        ),
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(to='webproject.Tag'),
        ),
    ]