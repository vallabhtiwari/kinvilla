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
    applicant = models.OneToOneField(Resident, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(auto_now_add=True)
    room_applied = models.CharField(max_length=3, default="---")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
