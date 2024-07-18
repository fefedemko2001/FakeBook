from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name + self.user.last_name} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)  # Call the parent class's save() method

        img = Image.open(self.image.path)

        if img.height > 750 or img.width > 750:
            output_size = (750, 750)
            img.thumbnail(output_size)
            img.save(self.image.path)

