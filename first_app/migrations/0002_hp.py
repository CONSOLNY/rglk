# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 07:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hp', models.IntegerField()),
                ('cell', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first_app.Cell')),
            ],
        ),
    ]
