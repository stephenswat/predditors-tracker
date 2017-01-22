# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-21 18:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('predds_tracker', '0004_auto_20170121_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='latest',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='predds_tracker.LocationRecord'),
            preserve_default=False,
        ),
    ]