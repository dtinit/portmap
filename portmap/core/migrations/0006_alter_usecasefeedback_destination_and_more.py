# Generated by Django 4.2.4 on 2024-03-07 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_usecasefeedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usecasefeedback',
            name='destination',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usecasefeedback',
            name='source',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
