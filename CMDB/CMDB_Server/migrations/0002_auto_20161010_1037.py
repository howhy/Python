# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-10 02:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMDB_Server', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='release_date',
            field=models.DateField(max_length=32, null=True),
        ),
    ]