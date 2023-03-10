# Generated by Django 3.2.9 on 2022-10-27 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('learner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('course_img', models.ImageField(blank=True, null=True, upload_to='')),
                ('total_point', models.PositiveIntegerField(default=100)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('enrolled_users', models.ManyToManyField(related_name='students', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField(blank=True, null=True)),
                ('point', models.PositiveIntegerField(default=10)),
                ('posted', models.DateTimeField(auto_now_add=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commonapps.course')),
                ('submitted_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LearnerScores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(default=0)),
                ('graded_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('answers', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='commonapps.answers')),
                ('learner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commonapps.track'),
        ),
        migrations.AddField(
            model_name='course',
            name='tutor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='module_images')),
                ('video', models.FileField(blank=True, null=True, upload_to='module_videos')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commonapps.module')),
            ],
        ),
        migrations.AddField(
            model_name='answers',
            name='module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='commonapps.content'),
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('body', models.TextField(max_length=500)),
                ('posted', models.DateTimeField(auto_now_add=True, null=True)),
                ('Poster', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
