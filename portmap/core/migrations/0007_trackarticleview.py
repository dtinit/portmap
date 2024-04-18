# Generated by Django 4.2.4 on 2024-04-18 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_usecasefeedback_destination_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackArticleView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('article_path', models.CharField(max_length=100)),
                ('visited_directly', models.BooleanField(default=False)),
                ('external_referrer', models.URLField(blank=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.article')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
