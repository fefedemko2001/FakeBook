from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserProfileRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, Friend_Request
from book.urls import urlpatterns

def register(request):
    if request.method == 'POST':
        form = UserProfileRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserProfileRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

@login_required
def send_friend_request(request, userID):
    from_user_profile = Profile.objects.get(user=request.user)
    to_user_profile = Profile.objects.get(id=userID)
    friend_request, created = Friend_Request.objects.get_or_create(
        from_user=from_user_profile, to_user=to_user_profile)
    if created:
        messages.success(request, 'Friend request sent')
    else:
        messages.info(request, 'Friend request was already sent')
    return redirect('book-home')

@login_required
def accept_friend_request(request, requestID):
    try:
        friend_request = Friend_Request.objects.get(id=requestID)
    except Friend_Request.DoesNotExist:
        messages.error(request, 'Friend request not found')
        return redirect('user-posts', username=request.user.username)

    if friend_request.to_user.user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        messages.success(request, 'Friend request accepted')
    else:
        messages.error(request, 'Friend request not accepted')
    
    return redirect('user-posts', username=request.user.username)

@login_required
def decline_friend_request(request, requestID):
    try:
        friend_request = Friend_Request.objects.get(id=requestID)
    except Friend_Request.DoesNotExist:
        messages.error(request, 'Friend request not found')
        return redirect('user-posts', username=request.user.username)

    if friend_request.to_user.user == request.user:
        friend_request.delete()
        messages.success(request, 'Friend request declined')
    else:
        messages.error(request, 'Friend request not declined')
    
    return redirect('user-posts', username=request.user.username)

