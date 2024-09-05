from django.db import models
from users.models import Profile

class ChatMessage(models.Model):
    body = models.TextField()
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='msg_sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='msg_receiver')
    seen = models.BooleanField(default=False)

    def __str__(self):
       return self.body 