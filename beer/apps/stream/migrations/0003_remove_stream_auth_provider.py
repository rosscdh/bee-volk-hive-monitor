# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0002_stream_data_sources'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stream',
            name='auth_provider',
        ),
    ]
