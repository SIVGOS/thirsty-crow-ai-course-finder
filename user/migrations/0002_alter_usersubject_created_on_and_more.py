# Generated by Django 5.0.6 on 2024-09-30 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersubject',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='usertopic',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
