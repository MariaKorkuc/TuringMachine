# Generated by Django 3.1.2 on 2020-12-15 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TuringSimulator', '0007_auto_20201215_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='exampledb',
            name='example_steps',
            field=models.TextField(default=''),
        ),
    ]