from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone

class Trip(models.Model):
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='trip_images', null=True, blank=True)
  # Optional trip image
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    participants = models.ManyToManyField(User, related_name='joined_trips', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """Custom validation for date fields"""
        if self.start_date < timezone.now().date():
            raise ValidationError("Start date cannot be in the past.")
        if self.end_date < self.start_date:
            raise ValidationError("End date must be after start date.")

    def __str__(self):
        return f'{self.destination} ({self.start_date} to {self.end_date})'

    def get_absolute_url(self):
        return reverse('trip-detail', kwargs={'pk': self.pk})

    def is_active(self):
        """Check if the trip is still ongoing or upcoming"""
        return self.end_date >= timezone.now().date()
