# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FriendRequest, Friendship
from django.contrib.auth.models import User

@login_required
def send_friend_request(request, user_id):
    user = get_object_or_404(User, id=user_id)
    FriendRequest.objects.create(from_user=request.user, to_user=user)
    return redirect('user-posts', username=user.username)

def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        friend_request.accept()
    return redirect('friend_requests')

def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        friend_request.reject()
    return redirect('friend_requests')


def friend_requests(request):
    received_requests = FriendRequest.objects.filter(to_user=request.user, is_active=True)
    
    context = {
        'received_requests': received_requests,
    }
    
    return render(request, 'friends/friend_requests.html', context)