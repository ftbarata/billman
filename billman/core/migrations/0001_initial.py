# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-19 02:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Usuário')),
                ('contacts', models.TextField(blank=True, max_length=500, null=True, verbose_name='Contatos')),
            ],
            options={
                'verbose_name': 'Contato do administrador',
                'verbose_name_plural': 'Contatos dos administradores',
            },
        ),
    ]
