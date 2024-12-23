# Generated by Django 5.1.2 on 2024-11-02 22:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('location', models.CharField(max_length=254)),
                ('tel', models.CharField(max_length=254)),
                ('description', models.TextField()),
                ('working_hours', models.CharField(max_length=254)),
                ('type', models.CharField(choices=[('business', 'Business'), ('customer', 'Customer')], max_length=254)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]
