# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-23 03:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20161209_0822'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]