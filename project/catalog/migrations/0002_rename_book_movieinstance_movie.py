# Generated by Django 4.1 on 2022-09-04 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movieinstance',
            old_name='book',
            new_name='movie',
        ),
    ]