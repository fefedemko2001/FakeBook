from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserProfileRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, Friend_Request
from book.urls import urlpatterns

def register(request):
    if request.method == 'POST':
        form = UserProfileRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                age=form.cleaned_data['age'],
                gender=form.cleaned_data['gender'],
                location=form.cleaned_data['location'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                image=form.cleaned_data.get('image', 'default.jpg')
            )
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
    to_user_profile = get_object_or_404(Profile, id=userID)
    from_user_profile = request.user.profile

    if to_user_profile != from_user_profile:
        from_user_profile.friends.add(to_user_profile)
        to_user_profile.friends.add(from_user_profile)
        messages.success(request, f'Friend request sent to {to_user_profile.user.username}')
    else:
        messages.error(request, "You cannot send a friend request to yourself")

    return redirect('profile')

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

