from django.shortcuts import render
from .models import Post

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'book/home.html', context)

def about(request):
    return render(request, 'book/about.html', {'title':'about'})
# Create your views here.
