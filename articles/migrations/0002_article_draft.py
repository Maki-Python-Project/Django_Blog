# Generated by Django 3.2 on 2022-08-05 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='draft',
            field=models.BooleanField(default=False),
        ),
    ]