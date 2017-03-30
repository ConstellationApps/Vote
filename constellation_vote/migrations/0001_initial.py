# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-29 04:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ballot',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('selected_options', models.TextField()),
                ('owned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('starts', models.DateTimeField()),
                ('ends', models.DateTimeField()),
                ('archived', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='PollOption',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=75)),
                ('desc', models.TextField()),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='constellation_vote.Poll')),
            ],
        ),
        migrations.AddField(
            model_name='ballot',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='constellation_vote.Poll'),
        ),
    ]
