# Generated by Django 4.2.3 on 2023-07-04 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user',
            new_name='creator',
        ),
    ]
