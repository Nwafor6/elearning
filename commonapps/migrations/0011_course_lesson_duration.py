# Generated by Django 3.2.9 on 2023-02-06 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapps', '0010_auto_20230201_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='lesson_duration',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
