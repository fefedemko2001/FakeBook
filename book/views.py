from django.shortcuts import render

posts = [
    {
        'author':'Ferike',
        'title':'Elso bejegy',
        'content': 'valami',
        'date_posted':'2024 01 08'
    },
    {
        'author':'Anna',
        'title':'Masodik bejegy',
        'content': 'valami2',
        'date_posted':'2024 01 10'
    }
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'book/home.html', context)

def about(request):
    return render(request, 'book/about.html', {'title':'about'})
# Create your views here.
