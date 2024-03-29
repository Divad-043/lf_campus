# Generated by Django 4.1.5 on 2023-04-12 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_depositpoint_location_depositpoint_latitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='found_location',
        ),
        migrations.RemoveField(
            model_name='item',
            name='lost_location',
        ),
        migrations.AddField(
            model_name='item',
            name='found_location_latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='found_location_longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='lost_location_latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='lost_location_longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
