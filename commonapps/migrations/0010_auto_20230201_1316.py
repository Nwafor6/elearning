# Generated by Django 3.2.9 on 2023-02-01 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapps', '0009_alter_learnerscores_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='duration',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='level',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
