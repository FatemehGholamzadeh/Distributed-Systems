# Generated by Django 2.1.7 on 2019-04-04 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='test_file_input',
            new_name='test_file',
        ),
        migrations.RemoveField(
            model_name='problem',
            name='test_file_output',
        ),
    ]
