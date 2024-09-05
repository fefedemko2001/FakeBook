import json
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import ChatMessage
from .froms import ChatMessageFrom

@login_required
def chat(request):
    user = request.user
    friends = user.get_friends()
    
    context = {
        'user': user,
        'friends': friends
    }
    
    return render(request, 'chat/chat.html', context)

@login_required
def detail(request, username):
    user_profile = get_object_or_404(Profile, user=request.user)
    friend_profile = get_object_or_404(Profile, user__username=username)  
    chats = ChatMessage.objects.all()
    received_chats = ChatMessage.objects.filter(sender = friend_profile, receiver = user_profile)
    received_counter = received_chats.count()
    received_chats.update(seen=True)

    form = ChatMessageFrom()
    if request.method == 'POST':
        form = ChatMessageFrom(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = user_profile
            message.receiver = friend_profile
            message.save()
            return redirect('detail', username)
    context = {
        'user_profile': user_profile,
        'friend_profile': friend_profile,
        'form': form,
        'chats': chats,
        'cnt': received_counter
    }

    return render(request, 'chat/detail.html', context)

def sentMessages(request, username):
    data = json.loads(request.body)
    new_chat = data['msg']
    print(new_chat)
    sender = request.user.profile
    friend = User.objects.get(username = username).profile
    new_chat_message = ChatMessage.objects.create(body=new_chat, sender=sender, receiver=friend, seen=False)
    return JsonResponse(new_chat_message.body, safe=False)

def receivedMessages(request, username):
    sender = User.objects.get(username = username).profile
    receiver = request.user.profile
    chatmessages = ChatMessage.objects.filter(sender = sender, receiver = receiver)
    arr = []
    for chat in chatmessages:
        arr.append(chat.body)
    return JsonResponse(arr, safe=False)

def chatNotification(request):
    user = request.user
    friends = user.get_friends()
    notifications = []
    for friend in friends:
        chats = ChatMessage.objects.filter(sender = friend.profile, receiver = request.user.profile , seen=False)
        notifications.append(chats.count())
    return JsonResponse(notifications, safe=False)