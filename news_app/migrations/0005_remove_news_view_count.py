# Generated by Django 5.1.1 on 2024-09-27 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0004_news_view_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='view_count',
        ),
    ]
