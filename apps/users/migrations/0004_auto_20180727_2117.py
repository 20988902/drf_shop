# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-27 21:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180727_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='出生年月'),
        ),
    ]