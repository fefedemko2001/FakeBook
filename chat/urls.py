from django.urls import path
from .views import chat, detail, sentMessages, receivedMessages, chatNotification


urlpatterns = [
    path('chat/', chat, name = 'chat'),
    path('detail/<str:username>/', detail, name='detail'),
    path('sent_msg/<str:username>/', sentMessages, name = 'sent_msg'),
    path('recv_msg/<str:username>/', receivedMessages, name = 'recv_msg'),
    path('notification/', chatNotification, name = 'notification')
]


