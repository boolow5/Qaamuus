# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-11 06:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [(b'dictionary', '0001_initial'), (b'dictionary', '0002_category_comment'), (b'dictionary', '0003_comment_about'), (b'dictionary', '0004_reaction'), (b'dictionary', '0005_auto_20170210_1743'), (b'dictionary', '0006_word_category'), (b'dictionary', '0007_auto_20170210_2055'), (b'dictionary', '0008_auto_20170210_2108')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
                ('definition', models.TextField(max_length=300)),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
                ('shares', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=300)),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
                ('shares', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('about', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dictionary.Word')),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('negative', models.BooleanField(default=False)),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dictionary.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('word', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dictionary.Word')),
            ],
        ),
        migrations.AddField(
            model_name='word',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dictionary.Category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='word',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='views',
            new_name='comments',
        ),
        migrations.RenameField(
            model_name='word',
            old_name='views',
            new_name='comments',
        ),
    ]
