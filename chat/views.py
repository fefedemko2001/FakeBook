from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from users.models import Profile
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
        'chats': chats
    }

    return render(request, 'chat/detail.html', context)