# Generated by Django 4.0.2 on 2023-06-13 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventsApp', '0005_venue_venue_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='approved_yes_no',
            field=models.BooleanField(default=False, verbose_name='Approved'),
        ),
    ]
