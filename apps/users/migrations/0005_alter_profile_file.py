# Generated by Django 5.1.2 on 2024-11-05 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_first_name_profile_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='file',
            field=models.ImageField(blank=True, null=True, upload_to='images/profiles/'),
        ),
    ]
