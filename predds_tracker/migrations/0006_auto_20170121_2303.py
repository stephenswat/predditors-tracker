# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-21 23:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('predds_tracker', '0005_character_latest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='latest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='predds_tracker.LocationRecord'),
        ),
    ]