# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20150721_1946'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='zop_code',
            new_name='zip_code',
        ),
    ]
