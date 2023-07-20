import csv
import io

from django.shortcuts import render, get_object_or_404, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm,EventForm,EventFormAdmin
from django.http import HttpResponseRedirect, HttpResponse
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.contrib import messages
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator
from django.contrib.auth.models import User


# Create your views here.
def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)

    venue_owner = User.objects.get(pk=venue.owner)
    # grab events from the venue id
    events = venue.event_set.all()
    return render(request, 'EventsApp/show_venue.html', {
        'venue': venue,
        'venue_owner': venue_owner,
        'events': events,
    })

def Home(request, year=datetime.now().year,month=datetime.now().strftime('%B')):
    name = "James Okuku"
    month = month.title()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    #create calender
    cal = HTMLCalendar().formatmonth(
        year,
        month_number
    )
    #get current year
    now = datetime.now()
    current_year = now.year

    event_list = Event.objects.filter(
        event_date__year = year,
        event_date__month = month_number
    )
    #get current time
    time = now.strftime('%I:%M:%S %p')
    return render(request, 'EventsApp/home.html', {
        'name': name,
        'year': year,
        'month': month,
        "month_number": month_number,
        'cal': cal,
        'current_year':current_year,
        'time': time,
        'event_list': event_list

    })


def all_events(request):
    event_list = Event.objects.all().order_by('-name')
    return render(request, 'EventsApp/event_list.html', {
        'event_list':event_list
    })

def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id #login id, venue.owner comes from the model
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'EventsApp/add_venue.html', {
        'form':form,
        'submitted':submitted
    })

def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('venue_list')
    return render(request, 'EventsApp/update_venue.html', {
        'venue':venue,
        'form':form
    })

def venue_list(request):
    venue_list = Venue.objects.all().order_by('name')
    #set up pagination
    p = Paginator(Venue.objects.all(), 2)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages  # a is just any string. you can use any letter
    # when a is multiplied it will give us a string of e.g aaaa which will be counted by forloops
    return render(request, 'EventsApp/venues.html', {
        'venue_list': venue_list,
        'venues': venues,
        'nums': nums,
    })

def venue_events(request, venue_id):
    venue = Venue.objects.get(id=venue_id)
    events = venue.event_set.all()
    return render(request, 'EventsApp/venue_events.html', {
        'events':events
    })

def Search_Venue(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__icontains=searched)
        return render(request, 'EventsApp/search_venue.html', {
            'searched':searched,
            'venues':venues,
        })
    else:
        return render(request, 'EventsApp/search_venue.html', {})

def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user #logged in user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'EventsApp/add_event.html', {
        'form': form,
        'submitted': submitted
    })

def Update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)  #  // instance will fill out the form texts with values
    else:
        form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, 'EventsApp/update_event.html', {
        'event': event,
        'form': form
    })

def  Delete_Event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, 'Event Deleted Succeessfully!')
        return redirect('event_list')
    else:
        messages.success(request,'You are not authorised to delete this event')
        return redirect('event_list')

def  Delete_Venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('venue_list')

def Venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    #designate venue model
    venues = Venue.objects.all()
    #create blank list
    lines = []
    # lines = ["This is line 1\n",
    #          "This is line 2\n",
    #          "This is line 3\n"]
    #loop through
    for venue in venues:
        lines.append(f'{venue}\n{venue.address}\n\n')
    response.writelines(lines)
    return response

def Venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    # create csv writer
    writer = csv.writer(response)
    #designate venue model
    venues = Venue.objects.all()
    #add column header
    writer.writerow(['Venue Name', 'Address'])

    for venue in venues:
        writer.writerow([venue.name,venue.address])
    return response

def Venue_pdf(request):
    #create bytestream buffer
    buf = io.BytesIO()
    #create canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #create text
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    #add some lines of texts

    # lines = [
    #     "This is Line 1",
    #     "This is Line 2",
    #     "This is Line 3",
    # ]
    venues = Venue.objects.all()
    lines = []
    #loop
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.email_address)
        lines.append("")

    for line in lines:
        textob.textLine(line)
    #finnish
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    #return
    return FileResponse(buf, as_attachment=True, filename='Venues.pdf')

def my_events(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        events = Event.objects.filter(attendees=user_id)
        return render(request, 'EventsApp/my_events.html', {
            'events':events,
            'user_id':user_id
        })
    else:
        messages.success(request,'You are Not authorised to View this Page')
        return redirect('home')

def search_event(request):
    if request.method == "POST":
        searched = request.POST['searched']
        events = Event.objects.filter(name__icontains=searched)
        return render(request, 'EventsApp/search_event.html', {
            'searched': searched,
            'events': events,
        })
    else:
        return render(request, 'EventsApp/search_event.html', {})

def admin_approval(request):
    # Get Venue List
    venue_list = Venue.objects.all()
    # count events and venues and users
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()

    event_list = Event.objects.all().order_by('-event_date')
    if request.user.is_superuser:
        if request.method == "POST":
            id_list = request.POST.getlist('boxes')  # checkboxes were named boxes if from the html page
            # uncheck all Events
            event_list.update(approved_yes_no=False)
            # print(id_list) # this will show ids in the terminal
            # update datebase with ids found
            for x in id_list:
                Event.objects.filter(pk=int(float(x))).update(approved_yes_no=True)

            messages.success(request, ("Event Approved"))
            return redirect('event_list')
        else:
            return render(request, 'EventsApp/admin_approval_page.html', {
                'event_list': event_list,
                'event_count':event_count,
                'venue_count': venue_count,
                'user_count': user_count,
                'venue_list': venue_list,
        })
    else:
        messages.success(request, 'Your are not allowed to view this page')
        return redirect('home')

    return render(request, 'EventsApp/admin_approval_page.html', {})

# Show Events in The Selected Venue
def show_venue_events(request, venue_id):
    # get venue id
    venue = Venue.objects.get(id=venue_id)
    # grab events from the venue id
    events = venue.event_set.all()
    if events:
        return render(request, 'EventsApp/event_venue_list.html', {
            'events': events,
    })
    else:
        messages.success(request, "That Venue has no Events")
        return redirect('admin_approval')

# after getting events in the venue
# show venue details

def show_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'EventsApp/show_event.html', {
        'event': event,
    })



