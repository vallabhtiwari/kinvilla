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
    address = models.CharField(max_length=100)
    profession = models.CharField(max_length=50, null=True, blank=True)
    work_address = models.CharField(max_length=100, null=True, blank=True)
    room = models.OneToOneField(Room, null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        if self.room:
            self.room.occupied = True
            self.room.save()
        super(Resident, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}"
