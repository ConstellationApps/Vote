# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-02 01:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0008_alter_user_username_max_length'),
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
                ('desc', models.TextField(blank=True, null=True)),
                ('starts', models.DateTimeField(auto_now=True)),
                ('ends', models.DateTimeField(blank=True, null=True)),
                ('results_visible', models.BooleanField(default=False)),
                ('archived', models.BooleanField(default=False)),
                ('owned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            options={
                'permissions': (('poll_owned_by', 'Poll Owner'), ('poll_visible_to', 'Poll is Visible')),
            },
        ),
        migrations.CreateModel(
            name='PollOption',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=75)),
                ('desc', models.TextField(blank=True, null=True)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='constellation_vote.Poll')),
            ],
        ),
        migrations.AddField(
            model_name='ballot',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='constellation_vote.Poll'),
        ),
    ]
