# Generated by Django 3.2 on 2022-08-12 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_alter_article_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='views',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
