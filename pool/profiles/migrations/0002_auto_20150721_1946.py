# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='ovner',
            new_name='owner',
        ),
        migrations.AlterField(
            model_name='coursetype',
            name='name',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
