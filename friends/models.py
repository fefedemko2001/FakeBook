# friends/models.py
from django.contrib.auth.models import User
from django.db import models

class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friendships1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friendships2', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1.username} and {self.user2.username} are friends"

    class Meta:
        unique_together = ('user1', 'user2')

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  
    def accept(self):
        self.is_active = False
        self.save()
        
        if not Friendship.objects.filter(user1=self.from_user, user2=self.to_user).exists() and \
           not Friendship.objects.filter(user1=self.to_user, user2=self.from_user).exists():
            Friendship.objects.create(user1=self.from_user, user2=self.to_user)

    def reject(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"From {self.from_user.username} to {self.to_user.username}"
