# Generated by Django 2.2.2 on 2019-06-15 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_auto_20190615_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='published_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]