import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Status(models.TextChoices):
    Occupied = 'OCCUPIED', 'مشغول'
    Unoccupied = 'UNOCCUPIED', 'غير مشغول'

class OperationType(models.TextChoices):
    RENTING = 'RENTING', 'إيجار'
    SELLING = 'SELLING', 'بيع'

class Faces(models.IntegerChoices):
    one = 1, '1'
    two = 2, '2'
    three = 3, '3'
    four = 4, '4'


class House(models.Model):
    operationType = models.CharField(max_length=10, choices=OperationType.choices, default=OperationType.RENTING)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    pub_date = models.DateTimeField(default=timezone.now)
    length = models.FloatField(max_length=5)
    width = models.FloatField(max_length=5)
    faces = models.IntegerField(choices=Faces.choices, default=Faces.two)
    state = models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    municipality = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.Unoccupied)
    available_from = models.DateField(
        null=True,
        blank=True,
        help_text="If the house is in use, specify when it will be unoccupied."
    )
    access_hash = models.CharField(max_length=32, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.access_hash:
            self.access_hash = uuid.uuid4().hex[:32]
        super().save(*args, **kwargs)

    def clean(self):
        if self.status == Status.Occupied and not self.available_from:
            raise ValidationError({"available_from": "You must provide a date when the house will be unoccupied."})

        if self.status == Status.Unoccupied and self.available_from:
            raise ValidationError({"available_from": "Available from should be empty if the house is already unoccupied."})

    def __str__(self):
        return self.title

class HouseImage(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='house_images/')
    caption = models.CharField(max_length=255, blank=True)

