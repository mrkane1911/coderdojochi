# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-18 00:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coderdojochi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('ip', models.CharField(blank=True, max_length=255, null=True)),
                ('check_in', models.DateTimeField(blank=True, null=True)),
                ('affiliate', models.CharField(blank=True, max_length=255, null=True)),
                ('order_number', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('week_reminder_sent', models.BooleanField(default=False)),
                ('day_reminder_sent', models.BooleanField(default=False)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coderdojochi.Meeting')),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coderdojochi.Mentor')),
            ],
            options={
                'verbose_name': 'meeting order',
                'verbose_name_plural': 'meeting orders',
            },
        ),
        migrations.CreateModel(
            name='MentorOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('ip', models.CharField(blank=True, max_length=255, null=True)),
                ('check_in', models.DateTimeField(blank=True, null=True)),
                ('affiliate', models.CharField(blank=True, max_length=255, null=True)),
                ('order_number', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('week_reminder_sent', models.BooleanField(default=False)),
                ('day_reminder_sent', models.BooleanField(default=False)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coderdojochi.Mentor')),
            ],
            options={
                'verbose_name': 'mentor order',
                'verbose_name_plural': 'mentor orders',
            },
        ),
        migrations.RemoveField(
            model_name='session',
            name='mentors',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='mentors',
        ),
        migrations.AddField(
            model_name='mentororder',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coderdojochi.Session'),
        ),
    ]
