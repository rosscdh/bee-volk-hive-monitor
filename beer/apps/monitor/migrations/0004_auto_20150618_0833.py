# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_auto_20150618_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitorsite',
            name='task',
            field=models.ForeignKey(to='djcelery.PeriodicTask', blank=True),
        ),
    ]
