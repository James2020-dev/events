from datetime import date

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField('Address', max_length=100, blank=True)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField('Contact', max_length=100)
    web = models.URLField('Web site Addres', max_length=100, blank=True)
    email_address = models.EmailField('Email Address', blank=True)
    owner = models.IntegerField('Venue Owner', blank=False, default=1)
    venue_image = models.ImageField(blank=True, null=True, upload_to="images/")

    def __str__(self):
        return self.name

class ClubUsers(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('Email', blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Event(models.Model):
    name = models.CharField('Event Name', max_length=100)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, blank=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(ClubUsers, blank=True)
    approved_yes_no = models.BooleanField('Approved', default=False)

    def __str__(self):
        return self.name

    @property
    def Days_rem(self):  # Days_rem if the name of the function that will be called on the form
        today = date.today()
        days_rem = self.event_date.date() - today
        days_rem_stripped = str(days_rem).split(",", 1)[0]
        return days_rem_stripped

    @property
    def Is_Days_Past(self):
        today = date.today()
        if self.event_date.date() < today:
            info = "Past"
        else:
            info = "Future"
        return info


