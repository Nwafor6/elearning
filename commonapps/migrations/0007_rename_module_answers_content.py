# Generated by Django 3.2.9 on 2022-10-29 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commonapps', '0006_module_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answers',
            old_name='module',
            new_name='Content',
        ),
    ]
