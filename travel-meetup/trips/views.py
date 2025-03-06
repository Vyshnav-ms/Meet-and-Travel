from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Trip
from .forms import TripForm, TripSearchForm

def home(request):
    """
    Display the homepage with up to 6 recent active trips.
    Renders home.html by default at the root URL.
    """
    try:
        trips = Trip.objects.filter(
            end_date__gte=timezone.now().date()
        ).order_by('-created_at')[:6]
    except Exception as e:
        trips = []
        messages.error(request, f"Error loading trips: {str(e)}")
    
    context = {
        'trips': trips
    }
    return render(request, 'home.html', context)

class TripListView(ListView):
    """
    List all active trips with pagination and optional search filters.
    """
    model = Trip
    template_name = 'trips/trip_list.html'
    context_object_name = 'trips'
    paginate_by = 9
    
    def get_queryset(self):
        # Base queryset: active trips sorted by creation date
        queryset = Trip.objects.filter(
            end_date__gte=timezone.now().date()
        ).order_by('-created_at')
        
        # Apply search filters if provided
        form = TripSearchForm(self.request.GET)
        if form.is_valid():
            destination = form.cleaned_data.get('destination')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            
            if destination:
                queryset = queryset.filter(destination__icontains=destination)
            if start_date:
                queryset = queryset.filter(start_date__gte=start_date)
            if end_date:
                queryset = queryset.filter(end_date__lte=end_date)
                
        return queryset
    
    def get_context_data(self, **kwargs):
        # Add search form to context for template rendering
        context = super().get_context_data(**kwargs)
        context['search_form'] = TripSearchForm(self.request.GET)
        return context

class UserTripListView(LoginRequiredMixin, ListView):
    """
    List trips created by the logged-in user with pagination.
    Includes both active and past trips.
    """
    model = Trip
    template_name = 'trips/user_trips.html'
    context_object_name = 'trips'
    paginate_by = 5
    
    def get_queryset(self):
        return Trip.objects.filter(
            creator=self.request.user
        ).order_by('-created_at')

class TripDetailView(DetailView):
    """
    Display details of a specific trip.
    """
    model = Trip
    template_name = 'trips/trip_detail.html'

class TripCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new trip, restricted to logged-in users.
    """
    model = Trip
    form_class = TripForm
    template_name = 'trips/trip_form.html'
    
    def form_valid(self, form):
        # Assign the current user as the trip creator
        form.instance.creator = self.request.user
        messages.success(self.request, 'Your trip has been created!')
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirect to the trip's detail page after creation
        return self.object.get_absolute_url()

class TripUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update an existing trip, restricted to the trip's creator.
    """
    model = Trip
    form_class = TripForm
    template_name = 'trips/trip_form.html'
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, 'Your trip has been updated!')
        return super().form_valid(form)
    
    def test_func(self):
        # Ensure only the creator can update the trip
        trip = self.get_object()
        return self.request.user == trip.creator
    
    def get_success_url(self):
        # Redirect to the trip's detail page after update
        return self.object.get_absolute_url()

class TripDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a trip, restricted to the trip's creator.
    """
    model = Trip
    template_name = 'trips/trip_confirm_delete.html'
    success_url = '/trips/'
    
    def test_func(self):
        # Ensure only the creator can delete the trip
        trip = self.get_object()
        return self.request.user == trip.creator
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your trip has been deleted!')
        return super().delete(request, *args, **kwargs)