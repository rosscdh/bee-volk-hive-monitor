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
                ('netloc', models.CharField(max_length=128, db_index=True)),
                ('name', models.CharField(max_length=128, db_index=True)),
                ('data', jsonfield.fields.JSONField(default={})),
                ('schedule', models.ForeignKey(blank=True, to='djcelery.IntervalSchedule', null=True)),
                ('task', models.ForeignKey(blank=True, to='djcelery.PeriodicTask', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(max_length=255, db_index=True)),
                ('scheme', models.CharField(max_length=10, null=True, db_index=True)),
                ('netloc', models.CharField(max_length=128, null=True, db_index=True)),
                ('path', models.CharField(max_length=128, null=True, db_index=True)),
                ('params', models.CharField(max_length=128, null=True, db_index=True)),
                ('query', models.CharField(max_length=128, null=True, db_index=True)),
                ('fragment', models.CharField(max_length=128, null=True, db_index=True)),
                ('data', jsonfield.fields.JSONField(default={})),
            ],
        ),
        migrations.CreateModel(
            name='UrlLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('digest', models.CharField(max_length=255, db_index=True)),
                ('date_of', models.DateTimeField(auto_now_add=True)),
                ('data', jsonfield.fields.JSONField(default={})),
                ('url', models.ForeignKey(to='monitor.Url')),
            ],
            options={
                'ordering': ('-date_of',),
            },
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
