from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager
from room.models import Room

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, primary_key=True)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Resident(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    profession = models.CharField(max_length=50, null=True, blank=True)
    work_address = models.CharField(max_length=100, null=True, blank=True)
    room = models.OneToOneField(Room, null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        super(Resident, self).save(*args, **kwargs)
        # first clearing the status of room in the database
        q = Resident.objects.filter(pk=self.pk)
        if q and q[0].room:
            q[0].room.occupied = False
            q[0].room.save()
        # setting occupied for correct room
        if self.room:
            self.room.occupied = True
            self.room.save()

    def __str__(self):
        return f"{self.user.first_name}"
