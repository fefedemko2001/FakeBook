from django import forms
from django.forms import ModelForm
from .models import ChatMessage

class ChatMessageFrom(ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['body',]