# Generated by Django 4.2.4 on 2023-12-11 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueryLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('datatype', models.CharField(max_length=30)),
                ('source', models.TextField(max_length=100)),
                ('destination', models.TextField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
