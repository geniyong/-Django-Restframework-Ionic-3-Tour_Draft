# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-31 08:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('_Item', '0004_item_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distance',
            name='dst',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dst', to='_Item.City'),
        ),
        migrations.AlterField(
            model_name='distance',
            name='src',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='src', to='_Item.City'),
        ),
    ]
