# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0004_auto_20150618_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitorsite',
            name='schedule',
            field=models.ForeignKey(blank=True, to='djcelery.IntervalSchedule', null=True),
        ),
        migrations.AlterField(
            model_name='monitorsite',
            name='task',
            field=models.ForeignKey(blank=True, to='djcelery.PeriodicTask', null=True),
        ),
    ]
