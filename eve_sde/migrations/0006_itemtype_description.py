# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 21:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eve_sde', '0005_remove_itemtype_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemtype',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]