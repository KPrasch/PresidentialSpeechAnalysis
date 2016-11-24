# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-24 07:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveSmallIntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Politician',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('birth_location', models.CharField(blank=True, max_length=1024, null=True)),
                ('birth_date', models.DateField()),
                ('deceased_date', models.DateField(blank=True, null=True)),
                ('political_party', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Speech',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1024, null=True)),
                ('body', models.TextField()),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='President',
            fields=[
                ('politician_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='profiles.Politician')),
                ('presidecy_number', models.PositiveSmallIntegerField()),
                ('presidency_start_year', models.DateTimeField()),
                ('presidency_end_year', models.DateTimeField()),
                ('ari_score', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('wordcloud', models.ImageField(upload_to=b'')),
            ],
            bases=('profiles.politician',),
        ),
        migrations.AddField(
            model_name='election',
            name='candidates',
            field=models.ManyToManyField(to='profiles.Politician'),
        ),
        migrations.AddField(
            model_name='election',
            name='vice_president_elect',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='election_as_vp', to='profiles.Politician'),
        ),
        migrations.AddField(
            model_name='speech',
            name='speaker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speeches', to='profiles.President'),
        ),
        migrations.AddField(
            model_name='election',
            name='president_elect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='election', to='profiles.President'),
        ),
    ]
