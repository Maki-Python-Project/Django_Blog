# Generated by Django 3.2 on 2022-08-08 23:32

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_remove_article_draft'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='article',
            managers=[
                ('draft_obj', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='draft',
            field=models.BooleanField(default=False),
        ),
    ]
