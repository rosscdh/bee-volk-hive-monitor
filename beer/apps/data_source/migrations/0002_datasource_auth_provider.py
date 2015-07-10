# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0003_alter_email_max_length'),
        ('data_source', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasource',
            name='auth_provider',
            field=models.ForeignKey(default=1, to='default.UserSocialAuth'),
            preserve_default=False,
        ),
    ]
