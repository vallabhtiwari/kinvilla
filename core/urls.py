from django.urls import path
from .views import CreateBookingView

app_name = "core"
urlpatterns = [
    path("create-booking/", CreateBookingView.as_view(), name="create-booking"),
]
