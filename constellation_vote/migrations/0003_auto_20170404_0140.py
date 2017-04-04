# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-04 01:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('constellation_vote', '0002_auto_20170402_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='owned_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]