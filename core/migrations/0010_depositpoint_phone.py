# Generated by Django 4.2 on 2023-04-24 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_itemquestiontag_remove_item_categories_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='depositpoint',
            name='phone',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
    ]
