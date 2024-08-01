from django.urls import path
from .views import chat, detail, sentMessages


urlpatterns = [
    path('chat/', chat, name = 'chat'),
    path('detail/<str:username>/', detail, name='detail'),
    path('sent_msg/<str:username>/', sentMessages, name = 'sent_msg')
]


