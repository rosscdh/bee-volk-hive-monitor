# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0003_alter_email_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField(max_length=128, null=True, blank=True)),
                ('data', jsonfield.fields.JSONField(default={})),
                ('auth_provider', models.ForeignKey(blank=True, to='default.UserSocialAuth', null=True)),
            ],
        ),
    ]
