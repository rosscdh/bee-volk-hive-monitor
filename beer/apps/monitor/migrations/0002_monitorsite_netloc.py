# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitorsite',
            name='netloc',
            field=models.CharField(default='None.com', max_length=128, db_index=True),
            preserve_default=False,
        ),
    ]
