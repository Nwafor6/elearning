# Generated by Django 3.2.9 on 2022-10-29 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commonapps', '0007_rename_module_answers_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answers',
            old_name='Content',
            new_name='content',
        ),
    ]
