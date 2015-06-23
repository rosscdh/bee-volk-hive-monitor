# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import beer.apps.role_permission.mixins
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_owner', models.BooleanField(default=False, db_index=True)),
                ('role', models.IntegerField(default=0, db_index=True, choices=[(0, b'No Access'), (1, b'Account Admin (brand)'), (2, b'Account Admin (print)'), (3, b'Brand Manager'), (4, b'Print Operator')])),
                ('data', jsonfield.fields.JSONField(default={})),
                ('site', models.ForeignKey(to='monitor.MonitorSite')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            bases=(beer.apps.role_permission.mixins.PermissionProviderMixin, models.Model),
        ),
    ]
