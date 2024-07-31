from django.urls import path
from .views import chat, detail


urlpatterns = [
    path('chat/', chat, name = 'chat'),
    path('detail/<str:username>/', detail, name='detail'),
]


