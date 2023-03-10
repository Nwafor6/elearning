# Generated by Django 3.2.9 on 2023-01-15 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapps', '0009_alter_learnerscores_answers'),
        ('accounts', '0006_rename_intrest_customuser_interest'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='github_repo',
            field=models.URLField(blank='', null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='linkedln_profile',
            field=models.URLField(blank='', null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='paid',
            field=models.BooleanField(blank='', default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone_numuber',
            field=models.CharField(blank='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='twitter_profile',
            field=models.URLField(blank='', null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='interest',
            field=models.ManyToManyField(blank='True', null=True, to='commonapps.Course'),
        ),
    ]
