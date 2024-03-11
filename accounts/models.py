from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    bio = models.CharField(max_length=255, blank=True)
    profile_img = models.ImageField(upload_to='users/profile_images', default='blank-profile-picture.webp')

    def save(self, *args, **kwargs):
        # If bio is not provided, set a default bio based on the username
        if not self.bio:
            self.bio = f"I'm {self.username}!"
        super().save(*args, **kwargs)