from django.db import models
import uuid

from user.models import Resident
from room.models import Room

# Create your models here.
class Payment(models.Model):
    payment_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    payer = models.ForeignKey(
        Resident, null=True, blank=True, on_delete=models.SET_NULL
    )
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    first_payment = models.BooleanField(default=False)
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)
