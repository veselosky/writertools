# Generated by Django 3.2.17 on 2023-02-11 12:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, max_length=4000, verbose_name='description')),
                ('per_row', models.PositiveSmallIntegerField(default=2, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(32)], verbose_name='sequences per row')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'board',
                'verbose_name_plural': 'boards',
            },
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, max_length=4000, verbose_name='description')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plotboard.board')),
            ],
            options={
                'verbose_name': 'sequence',
                'verbose_name_plural': 'sequences',
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, max_length=4000, verbose_name='description')),
                ('content', tinymce.models.HTMLField(blank=True, verbose_name='content')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plotboard.board')),
                ('sequence', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='plotboard.sequence')),
            ],
            options={
                'verbose_name': 'card',
                'verbose_name_plural': 'cards',
                'order_with_respect_to': 'sequence',
            },
        ),
    ]