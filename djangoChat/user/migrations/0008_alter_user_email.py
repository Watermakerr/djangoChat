# Generated by Django 5.0.1 on 2024-06-07 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_user_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
    ]
