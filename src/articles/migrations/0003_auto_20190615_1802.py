# Generated by Django 2.2.2 on 2019-06-15 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20190613_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='published_date',
            field=models.DateTimeField(blank=True),
        ),
    ]
