# Generated by Django 3.1.6 on 2021-03-02 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0003_problem_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='problem_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
