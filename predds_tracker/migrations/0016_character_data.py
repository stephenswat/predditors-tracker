# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 15:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_django', '0005_auto_20160727_2333'),
        ('predds_tracker', '0015_auto_20170127_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='data',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='social_django.UserSocialAuth'),
        ),
    ]