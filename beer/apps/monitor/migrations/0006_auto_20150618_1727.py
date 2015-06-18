# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0005_auto_20150618_0833'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='urllog',
            options={'ordering': ('-date_of',)},
        ),
    ]
