from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FriendRequest, Friendship
from django.contrib.auth.models import User
from django.db.models import Q

@login_required
def send_friend_request(request, user_id):
    user = get_object_or_404(User, id=user_id)

    existing_request = FriendRequest.objects.filter(from_user=request.user, to_user=user).first()
    if not existing_request:
        if not Friendship.objects.filter(user1=request.user, user2=user).exists() and not Friendship.objects.filter(user1=user, user2=request.user).exists():
            FriendRequest.objects.create(from_user=request.user, to_user=user)

    return redirect('user-posts', username=user.username)

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        friend_request.accept()
        Friendship.objects.get_or_create(user1=friend_request.from_user, user2=friend_request.to_user)
        friend_request.delete()

    return redirect('user-posts', username=friend_request.from_user.username)

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        friend_request.reject()
        friend_request.delete()

    return redirect('user-posts', username=friend_request.from_user.username)


def friend_requests(request):
    received_requests = FriendRequest.objects.filter(to_user=request.user, is_active=True)
    context = {
        'received_requests': received_requests,
    }    
    return render(request, 'friends/friend_requests.html', context)

@login_required
def find_friends(request):
    users = User.objects.exclude(id=request.user.id) 
    gender_filter = request.GET.get('gender', None)
    min_age = request.GET.get('min_age', None)
    max_age = request.GET.get('max_age', None)

    profile_filters = Q()
    if gender_filter:
        profile_filters &= Q(profile__gender=gender_filter)
    if min_age:
        profile_filters &= Q(profile__age__gte=min_age)
    if max_age:
        profile_filters &= Q(profile__age__lte=max_age)

    users = users.filter(profile_filters)

    friends_ids = set(Friendship.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).values_list('user1', 'user2'))
    friends_ids = set([user1_id if user1_id != request.user.id else user2_id for (user1_id, user2_id) in friends_ids])
    sent_requests_ids = set(FriendRequest.objects.filter(from_user=request.user, is_active=True).values_list('to_user', flat=True))
    received_requests = FriendRequest.objects.filter(to_user=request.user, is_active=True)
    received_requests_list = [
        {"request_id": request.id, "from_user_id": request.from_user.id}
        for request in received_requests
    ]

    if request.method == 'POST':
        to_user_id = request.POST.get('to_user')
        if to_user_id:
            to_user = User.objects.get(id=to_user_id)
            if not FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists() and \
               not Friendship.objects.filter(user1=request.user, user2=to_user).exists() and \
               not Friendship.objects.filter(user1=to_user, user2=request.user).exists():
                FriendRequest.objects.create(from_user=request.user, to_user=to_user)
            return redirect('find_friends') 

    context = {
        'users': users,
        'friends_ids': friends_ids,
        'sent_requests_ids': sent_requests_ids,
        'received_requests_list': received_requests_list,
    }
    return render(request, 'friends/find_friends.html', context)