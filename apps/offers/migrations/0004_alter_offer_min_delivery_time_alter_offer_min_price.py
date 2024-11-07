# Generated by Django 5.1.2 on 2024-11-07 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0003_alter_offerdetail_revisions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='min_delivery_time',
            field=models.PositiveIntegerField(editable=False, help_text='Minimum delivery time in days'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='min_price',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=10),
        ),
    ]