from django.shortcuts import redirect, render
from django.views.generic import View, CreateView
from django.urls import reverse_lazy

from .forms import UserRegisterForm
from .models import User

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
