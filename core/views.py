from django.shortcuts import redirect
from django.http import JsonResponse

from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, View, CreateView
from http import HTTPStatus
import json

from .models import Booking, Verification
from .forms import ResidentVerificationForm
from room.models import Room

# Create your views here.
class CreateBookingView(View):
    def post(self, request, *args, **kwargs):
        context = {
            "success": True,
            "redirect": False,
            "message": "Booking successful, please wait till it is confirmed...",
        }
        room_number = json.load(request).get("room_number")
        room = Room.objects.filter(room_number=room_number)
        if not room:
            context["success"] = False
            context["message"] = "Room with given room number does not exists"
            return JsonResponse(context, status=HTTPStatus.BAD_REQUEST)

        if room[0].occupied:
            context["success"] = False
            context["message"] = "Room is not vaccant"
            return JsonResponse(context, status=HTTPStatus.BAD_REQUEST)

        # if not verified stuff :
        if not Verification.objects.filter(person=request.user.resident):
            context["success"] = False
            context["redirect"] = True
            context["redirect_url"] = reverse("user:user-verification")
            context["message"] = "Applicant not verified"
            return JsonResponse(context, status=HTTPStatus.TEMPORARY_REDIRECT)

        old_bookings = Booking.objects.filter(applicant=request.user.resident).filter(
            status="0"
        )
        if old_bookings:
            context["success"] = False
            context["message"] = "Pending booking exists already"
            return JsonResponse(context, status=HTTPStatus.BAD_REQUEST)

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


class UpdateVerificationiView(UpdateView):
    fields = ["status"]
    model = Verification
    pk_url_kwarg = "resident_id"
    template_name = "core/resident_verification.html"
    success_url = reverse_lazy("user:admin-dashboard")


class UpdateBookingView(UpdateView):
    fields = ["room_applied", "status"]
    model = Booking
    pk_url_kwarg = "booking_id"
    template_name = "core/booking.html"
    success_url = reverse_lazy("user:admin-dashboard")

    def form_valid(self, form):
        booking = self.object
        verification = Verification.objects.filter(person=booking.applicant)
        if not verification.exists() or verification[0].status == "0":
            form.add_error(None, "Resident not verified")
            return self.form_invalid(form)

        current_room = Room.objects.filter(room_number=booking.room_applied)
        if not current_room:
            form.add_error(
                "room_applied", "Room with given room number does not exists"
            )
            return self.form_invalid(form)

        return super().form_valid(form)
