# Generated by Django 4.1.7 on 2023-07-01 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_movies_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='title',
            field=models.CharField(max_length=120, unique=True),
        ),
    ]
