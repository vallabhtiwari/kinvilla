from django.urls import path
from .views import CreateBookingView, UpdateBookingView, UpdateVerificationiView

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
        UpdateBookingView.as_view(),
        name="update-booking",
    ),
]
