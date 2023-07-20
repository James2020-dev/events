from django.contrib import admin
from django.urls import path,include
from . import views
import csv

urlpatterns = [
    path('', views.Home, name="home"),
    path('<int:year>/<str:month>/', views.Home, name='home'),
    path('event_list', views.all_events, name='event_list'),
    path('add_venue', views.add_venue, name='add_venue'),
    path('venue_list', views.venue_list, name='venue_list'),
    path('show_venue/<venue_id>/', views.show_venue, name='show_venue'),
    path('venue_events/<venue_id>', views.venue_events, name='venue_events'),
    path('search_venue', views.Search_Venue, name='search-venue'),
    path('update_venue/<venue_id>', views.update_venue, name='update_venue'),
    path('add_event', views.add_event, name='add_event'),
    path('update_event/<event_id>', views.Update_event, name='update_event'),
    path('delete_event/<event_id>/', views.Delete_Event, name='delete_event'),
    path('delete_venue/<venue_id>/', views.Delete_Venue, name='delete_venue'),
    path('venue_text', views.Venue_text, name='venue-text'),
    path('venue_csv', views.Venue_csv, name='venue-csv'),
    path('venue_pdc', views.Venue_pdf, name='venue-pdf'),
    path('my_events', views.my_events, name='my-events'),
    path('search_events', views.search_event, name='search-events'),
    path('admin_approval_page', views.admin_approval, name='admin_approval'),
    path('show_venue_events/<venue_id>/', views.show_venue_events, name='show_venue_events'),
    path('show_event/<event_id>/', views.show_event, name='show-event'),
]
