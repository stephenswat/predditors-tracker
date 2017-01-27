# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 15:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('predds_tracker', '0017_auto_20170127_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alt',
            name='data',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='social_django.UserSocialAuth'),
        ),
        migrations.AlterField(
            model_name='character',
            name='data',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='social_django.UserSocialAuth'),
        ),
    ]