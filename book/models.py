from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

class Image(models.Model):
    image = models.ImageField(upload_to='post_images/')
    description = models.CharField(max_length=255, blank=True, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_images')

    def __str__(self):
        return self.description or self.image.name
