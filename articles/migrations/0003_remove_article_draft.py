# Generated by Django 3.2 on 2022-08-05 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_draft'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='draft',
        ),
    ]
