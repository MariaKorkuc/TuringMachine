# Generated by Django 3.1.2 on 2020-12-05 23:57

import TuringSimulator.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TuringSimulator', '0004_auto_20201204_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turingmachinedb',
            name='instructions',
            field=models.FileField(default='excel_files/default_excel.xlsx', upload_to='excel_files', validators=[TuringSimulator.validators.validate_file_extension]),
        ),
    ]