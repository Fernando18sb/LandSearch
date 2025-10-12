import uuid

from django.db import models
from django.contrib.auth.models import User

class GeneratedCode(models.Model):
    code = models.CharField(max_length=5, null=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_num = models.CharField(max_length=10, blank=True)
    tg = models.CharField(
        max_length=30,
        help_text='Enter your Telegram username, That you want client to contact you on',
        blank=True,
    )
    fb = models.CharField(
        max_length=30,
        help_text='Enter your Facebook username, That you want client to contact you on',
        blank=True,
    )
    ig = models.CharField(
        max_length=30,
        help_text='Enter your Instagram username, That you want client to contact you on',
        blank=True,
    )
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    path = models.CharField(max_length=6, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.path is None:
            self.path = uuid.uuid4().hex[:6]
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} Profile'

