# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_source', '0002_datasource_auth_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasource',
            name='auth_provider',
            field=models.ForeignKey(blank=True, to='default.UserSocialAuth', null=True),
        ),
    ]
