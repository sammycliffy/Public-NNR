# Generated by Django 3.2 on 2021-09-24 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='contactPhone',
            field=models.CharField(max_length=255, null=True),
        ),
    ]