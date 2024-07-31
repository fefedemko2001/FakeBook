from datetime import date
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from PIL import Image
from friends.models import Friendship

class Profile(models.Model):
    GENDER_CHOICES = [
        ('man', 'Man'),
        ('woman', 'Woman'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs) 

        img = Image.open(self.image.path)
        if self.birthdate:
            today = date.today()
            self.age = today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))

        if img.height > 750 or img.width > 750:
            output_size = (750, 750)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_friends(self):
        friendships = Friendship.objects.filter(Q(user1=self) | Q(user2=self))
        friends = []
        for friendship in friendships:
            if friendship.user1 == self:
                friends.append(friendship.user2)
            else:
                friends.append(friendship.user1)
        return friends

    User.add_to_class('get_friends', get_friends)
