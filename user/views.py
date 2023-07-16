from django.shortcuts import redirect, render
from django.views.generic import View, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy

from .forms import UserRegisterForm, ResidentUpdateForm
from .models import User, Resident

# Create your views here.
class CreateUserView(CreateView):
    template_name = "user/register.html"
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("user:user-login")

    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        context = {
            "form": form,
        }
        return render(request, self.template_name, context)


class ResidentDetailView(DetailView):
    model = Resident
    slug_url_kwarg = "resident_id"
    slug_field = "resident_id"


class ResidentUpdateView(UpdateView):
    model = Resident
    form_class = ResidentUpdateForm
    template_name = "user/resident_update.html"
    success_url = reverse_lazy("user:user-login")

    def get(self, request, *args, **kwargs):
        form = ResidentUpdateForm(instance=request.user.resident)
        context = {
            "form": form,
        }
        return render(request, self.template_name, context)
