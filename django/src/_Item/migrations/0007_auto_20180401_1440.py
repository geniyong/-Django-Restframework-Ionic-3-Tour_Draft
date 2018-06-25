# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-01 05:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_Item', '0006_item_default_minute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='close_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='latitude',
            field=models.CharField(blank=True, max_length=45),
        ),
        migrations.AlterField(
            model_name='item',
            name='longitude',
            field=models.CharField(blank=True, max_length=45),
        ),
        migrations.AlterField(
            model_name='item',
            name='open_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='tel',
            field=models.CharField(blank=True, max_length=45),
        ),
    ]
