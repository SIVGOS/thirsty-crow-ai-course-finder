# Generated by Django 5.0.6 on 2024-10-12 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explore', '0002_subject_topics_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='tracking_id',
            field=models.UUIDField(null=True),
        ),
    ]
