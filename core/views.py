# from django.shortcuts import reverse, reverse_lazy
from django.http import JsonResponse

from django.urls import reverse, reverse_lazy
from django.views.generic import View, CreateView
from http import HTTPStatus
import json

from .models import Booking, Verification
from .forms import ResidentVerificationForm

# Create your views here.
class CreateBookingView(View):
    def post(self, request, *args, **kwargs):
        context = {
            "success": True,
            "redirect": False,
        }
        room_number = json.load(request).get("room_number")
        # if not verified stuff :
        if not Verification.objects.filter(person=request.user.resident):
            context["success"] = False
            context["redirect"] = True
            context["redirect_url"] = reverse("user:user-verification")

            return JsonResponse(context, status=HTTPStatus.TEMPORARY_REDIRECT)

        old_bookings = Booking.objects.filter(applicant=request.user.resident).filter(
            status="0"
        )
        if old_bookings:
            context["success"] = False
            return JsonResponse(context, status=HTTPStatus.TEMPORARY_REDIRECT)

        booking = Booking.objects.create(
            applicant=request.user.resident, room_applied=room_number
        )
        context["booking_id"] = booking.id

        return JsonResponse(context, status=HTTPStatus.OK)


class CreateResidentVerificationView(CreateView):
    model = Verification
    form_class = ResidentVerificationForm
    template_name = "core/resident_verification.html"

    def form_valid(self, form):
        form.instance.person = self.request.user.resident
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "user:user-detail",
            kwargs={"resident_id": self.request.user.resident.resident_id},
        )

    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)
