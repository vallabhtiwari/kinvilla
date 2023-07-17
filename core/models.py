from django.db import models
from user.models import Resident
import uuid

# Create your models here.
class Booking(models.Model):
    STATUS_CHOICES = [
        ("0", "In Process"),
        ("1", "Confirmed"),
    ]
    id = models.UUIDField(
        primary_key=True, unique=True, editable=False, default=uuid.uuid4
    )
    applicant = models.OneToOneField(Resident, null=True, on_delete=models.SET_NULL)
    date_applied = models.DateTimeField(auto_now_add=True)
    room_applied = models.CharField(max_length=3, default="xxx")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.applicant} -> {self.room_applied}"


class Verification(models.Model):
    ID_CHOICES = [
        ("1", "Institutional ID"),
        ("2", "Aadhar Number"),
        ("3", "Voter ID"),
        ("4", "Driving License"),
        ("5", "Passport"),
    ]
    STATUS_CHOICES = [
        ("0", "In Process"),
        ("1", "Verified"),
    ]
    person = models.OneToOneField(Resident, on_delete=models.CASCADE)
    id_type = models.CharField(max_length=1, choices=ID_CHOICES)
    id_number = models.CharField(max_length=50, primary_key=True, unique=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.person}"
