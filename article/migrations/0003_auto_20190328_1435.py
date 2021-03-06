# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2019-03-28 06:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0002_auto_20190328_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=500)),
                ('body', models.TextField(blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article', to=settings.AUTH_USER_MODEL)),
                ('column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_column', to='article.ArticleColumn')),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.AlterIndexTogether(
            name='aticlepost',
            index_together=set([]),
        ),
        migrations.RemoveField(
            model_name='aticlepost',
            name='author',
        ),
        migrations.RemoveField(
            model_name='aticlepost',
            name='column',
        ),
        migrations.DeleteModel(
            name='AticlePost',
        ),
        migrations.AlterIndexTogether(
            name='articlepost',
            index_together=set([('id', 'slug')]),
        ),
    ]
