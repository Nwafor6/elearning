# Generated by Django 3.2.9 on 2022-10-31 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commonapps', '0008_rename_content_answers_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learnerscores',
            name='answers',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='commonapps.answers'),
        ),
    ]