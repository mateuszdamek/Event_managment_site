# Generated by Django 5.0.4 on 2024-05-20 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(default='USER', max_length=50),
            preserve_default=False,
        ),
    ]
