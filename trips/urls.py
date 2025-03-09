from django.urls import path
from .views import (
    TripListView, UserTripListView, TripDetailView,
    TripCreateView, TripUpdateView, TripDeleteView
)

urlpatterns = [
    path('', TripListView.as_view(), name='trip-list'),
    path('my-trips/', UserTripListView.as_view(), name='my-trips'),  # ✅ Rename this
    path('<int:pk>/', TripDetailView.as_view(), name='trip-detail'),
    path('create/', TripCreateView.as_view(), name='trip-create'),
    path('<int:pk>/update/', TripUpdateView.as_view(), name='trip-update'),
    path('<int:pk>/delete/', TripDeleteView.as_view(), name='trip-delete'),
]
