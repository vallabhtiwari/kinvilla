from django.urls import path
from .views import RoomListView, RoomDetailView

app_name = "room"
urlpatterns = [
    path("floor/<str:floor>/", RoomListView.as_view(), name="room-list"),
    path(
        "floor/<str:floor>/<str:room_number>/",
        RoomDetailView.as_view(),
        name="room-detail",
    ),
]
