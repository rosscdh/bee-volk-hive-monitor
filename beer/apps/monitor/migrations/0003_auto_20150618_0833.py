# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_monitorsite_netloc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitorsite',
            name='schedule',
            field=models.ForeignKey(to='djcelery.IntervalSchedule', blank=True),
        ),
    ]
