# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('djcelery', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitorSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, db_index=True)),
                ('data', jsonfield.fields.JSONField(default={})),
                ('schedule', models.ForeignKey(to='djcelery.IntervalSchedule')),
                ('task', models.ForeignKey(to='djcelery.PeriodicTask')),
            ],
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(max_length=255, db_index=True)),
                ('schema', models.CharField(max_length=10, null=True, db_index=True)),
                ('host', models.CharField(max_length=128, null=True, db_index=True)),
                ('port', models.CharField(max_length=4, null=True, db_index=True)),
                ('query_string', models.CharField(max_length=255, null=True, db_index=True)),
                ('data', jsonfield.fields.JSONField(default={})),
            ],
        ),
        migrations.AddField(
            model_name='monitorsite',
            name='urls',
            field=models.ManyToManyField(to='monitor.Url'),
        ),
        migrations.AddField(
            model_name='monitorsite',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
