from .models import Venue,Event
from django import forms

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ('name','address','zip_code','phone','web','email_address','venue_image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Venue'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Zip Code'}),
            'web': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Web'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Description'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Adddress'}),
        }

class EventFormAdmin(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name','event_date','venue','manager','description','attendees','approved_yes_no')
        labels = {
            'name': '',
            'event_date': '',
            'venue': 'Venue',
            'manager': 'Manager',
            'description': '',
            'attendees': 'Attendees',
            'approved_yes_no': 'Approved_yes_no',

        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Venue'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date'}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Enter Venue'}),
            'manager': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Enter Zip Code'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Enter Attendees'}),
            # 'approved_yes_no': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Enter Attendees'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name','event_date','venue','description','attendees')
        labels = {
            'name': '',
            'event_date': '',
            'venue': 'Venue',
            'description': '',
            'attendees': 'Attendees',

        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Venue'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date'}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Enter Venue'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Enter Attendees'}),
        }
