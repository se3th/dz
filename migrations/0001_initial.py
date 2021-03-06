# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-08 15:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ComputerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=255)),
                ('picpath', models.CharField(blank=True, default='', max_length=255)),
            ],
            options={
                'db_table': 'my_app_computer',
            },
        ),
        migrations.CreateModel(
            name='CustomerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(default='', max_length=64)),
                ('secondname', models.CharField(default='', max_length=64)),
                ('firstname', models.CharField(default='', max_length=64)),
                ('email', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'my_app_customer',
            },
        ),
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_received', models.DateField()),
                ('date_completed', models.DateField()),
                ('status', models.BooleanField(default=False)),
                ('computer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.ComputerModel')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.CustomerModel')),
            ],
            options={
                'db_table': 'my_app_order',
            },
        ),
        migrations.AddField(
            model_name='customermodel',
            name='computers',
            field=models.ManyToManyField(through='my_app.OrderModel', to='my_app.ComputerModel'),
        ),
    ]
