# Generated by Django 3.2.20 on 2023-11-14 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('datatype', models.CharField(max_length=30)),
                ('sources', models.TextField(max_length=500)),
                ('destinations', models.TextField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
