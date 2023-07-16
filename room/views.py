from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Room

# Create your views here.
class RoomListView(ListView):
    model = Room

    def get_queryset(self):
        all_rooms = super().get_queryset()
        current_floor_rooms = all_rooms.filter(floor=self.kwargs.get("floor")).order_by(
            "occupied"
        )

        return current_floor_rooms


class RoomDetailView(DetailView):
    model = Room
    pk_url_kwarg = "room_number"
