# Generated by Django 5.1.1 on 2024-09-26 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_user_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
