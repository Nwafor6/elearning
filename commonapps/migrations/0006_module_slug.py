# Generated by Django 3.2.9 on 2022-10-29 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapps', '0005_module_submitted_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]