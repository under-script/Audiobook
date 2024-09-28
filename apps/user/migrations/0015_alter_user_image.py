# Generated by Django 5.1.1 on 2024-09-28 12:30

import apps.user.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='avatars/avatar_default.png', help_text='Upload an avatar image. If not provided, a default image will be used.', null=True, upload_to='avatars/', validators=[apps.user.validators.validate_image]),
        ),
    ]
