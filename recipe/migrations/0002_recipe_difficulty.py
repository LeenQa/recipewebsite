# Generated by Django 3.0.7 on 2020-06-16 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='difficulty',
            field=models.CharField(default='easy', max_length=50),
            preserve_default=False,
        ),
    ]
