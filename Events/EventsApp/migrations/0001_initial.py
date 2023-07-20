# Generated by Django 4.0.2 on 2023-05-21 06:46

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
            name='ClubUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Venue Name')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='Address')),
                ('zip_code', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=100, verbose_name='Contact')),
                ('web', models.URLField(blank=True, max_length=100, verbose_name='Web site Addres')),
                ('email_address', models.EmailField(blank=True, max_length=254, verbose_name='Email Address')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Event Name')),
                ('event_date', models.DateTimeField(verbose_name='Event Date')),
                ('description', models.TextField(blank=True)),
                ('attendees', models.ManyToManyField(blank=True, to='EventsApp.ClubUsers')),
                ('manager', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('venue', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='EventsApp.venue')),
            ],
        ),
    ]