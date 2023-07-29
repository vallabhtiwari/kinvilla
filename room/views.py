from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Room

# Create your views here.
class RoomListView(ListView):
    model = Room

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["room_list"] = (
            context["room_list"]
            .filter(floor=self.kwargs.get("floor"))
            .order_by("occupied")
        )
        context["floor"] = self.kwargs.get("floor")
        return context


class RoomDetailView(DetailView):
    model = Room
    pk_url_kwarg = "room_number"
