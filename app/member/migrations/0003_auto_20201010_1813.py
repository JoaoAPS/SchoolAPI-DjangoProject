# Generated by Django 3.1.2 on 2020-10-10 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_auto_20201010_1745'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='scholar_year',
            new_name='grade',
        ),
    ]
