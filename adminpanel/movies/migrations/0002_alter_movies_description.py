# Generated by Django 4.1.7 on 2023-07-01 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='description',
            field=models.TextField(),
        ),
    ]
