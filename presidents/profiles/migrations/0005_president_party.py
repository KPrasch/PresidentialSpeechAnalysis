# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-23 20:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_person_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='president',
            name='party',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]