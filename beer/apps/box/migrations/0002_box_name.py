# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('box', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='name',
            field=models.CharField(db_index=True, max_length=128, null=True, blank=True),
        ),
    ]
