from django.urls import path
from .views import (
    BookingListView,
)

app_name = "core"
urlpatterns = [
    path("create-booking/", CreateBookingView.as_view(), name="create-booking"),
    path(
        "update-verification/<str:resident_id>/",
        UpdateVerificationiView.as_view(),
        name="update-verification",
    ),
    path(
        "update-booking/<str:booking_id>/",
    path("my-bookings/", BookingListView.as_view(), name="my-bookings"),
    ),
]
