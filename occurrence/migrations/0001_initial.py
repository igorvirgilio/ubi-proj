# Generated by Django 3.0.5 on 2020-04-15 00:47

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Occurrence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_of_occur', models.CharField(choices=[('Construction', 'Construction'), ('Special Event', 'Special Event'), ('Incident', 'Incident'), ('Weather Condition', 'Weather Condition'), ('Road Condition', 'Road Condition')], max_length=17)),
                ('description', models.TextField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('author', models.TextField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Por Validar', 'Por validar'), ('Validado', 'Validado'), ('Resolvido', 'Resolvido')], default='Por Validar', max_length=11)),
            ],
        ),
    ]
