# Generated by Django 2.2.2 on 2019-06-16 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_auto_20190615_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=120, unique=True),
        ),
    ]
