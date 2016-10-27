# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 15:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('belt2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Add',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.CharField(max_length=255)),
                ('quote', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='belt2.Users')),
            ],
            managers=[
                ('quoteManager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='add',
            name='newquote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='belt2.Quotes'),
        ),
        migrations.AddField(
            model_name='add',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='belt2.Users'),
        ),
    ]
