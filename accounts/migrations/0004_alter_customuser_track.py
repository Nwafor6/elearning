# Generated by Django 3.2.9 on 2022-10-27 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapps', '0003_auto_20221027_1843'),
        ('accounts', '0003_alter_customuser_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='track',
            field=models.ManyToManyField(blank=True, null=True, to='commonapps.Track'),
        ),
    ]
