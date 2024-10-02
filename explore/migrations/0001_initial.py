# Generated by Django 5.0.6 on 2024-09-28 17:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=256)),
                ('experience_code', models.IntegerField(choices=[(1, 'I am completely new'), (2, 'I know some basics'), (3, 'Worked in the past but need to refresh')])),
                ('dedication_code', models.IntegerField(choices=[(1, 'I want to learn casually at my own pace'), (2, 'I am busy but I have dedicated time for learning'), (3, 'I am a full time learner')])),
                ('created_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'unique_together': {('subject_name', 'experience_code', 'dedication_code')},
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_name', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=256)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explore.subject')),
            ],
        ),
    ]