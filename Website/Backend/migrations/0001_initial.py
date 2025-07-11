# Generated by Django 5.2 on 2025-06-30 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, null=True)),
                ('name', models.CharField(default='LABEL', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeCreated', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('title', models.CharField(default='TITLE', max_length=200, null=True)),
                ('description', models.TextField(default='DESCRIPTION', max_length=500)),
                ('timeUpdated', models.DateTimeField(auto_now=True)),
                ('note', models.TextField(default='NOTE', max_length=300)),
                ('tags', models.ManyToManyField(blank=True, to='Backend.tag')),
            ],
        ),
    ]
