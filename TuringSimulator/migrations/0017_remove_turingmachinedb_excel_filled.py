# Generated by Django 3.1.2 on 2020-12-25 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TuringSimulator', '0016_turingmachinedb_excel_filled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turingmachinedb',
            name='excel_filled',
        ),
    ]
