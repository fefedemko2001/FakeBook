from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Post, Image


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'book/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        for file in self.request.FILES.getlist('file'):
            Image.objects.create(post=self.object, image=file)
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = False
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'book/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        # A képeket már elmentettük, így nincs szükség új mentésre
        return redirect(self.get_success_url())

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # A kapcsolódó képek hozzáadása a sablon kontextusához
        context['images'] = self.object.post_images.all()
        context['is_update'] = True
        return context


class PostListView(ListView):
    model = Post
    template_name = 'book/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class UserPostListView(ListView):
    model = Post
    template_name = 'book/user_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def home(request):
    posts = Post.objects.all()  # vagy bármilyen más módszerrel lekérheted a bejegyzéseket
    return render(request, 'book/home.html', {'posts': posts})

def about(request):
    return render(request, 'book/about.html', {'title': 'about'})

class PostLikeView(View):
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        post.likes += 1
        post.save()
        return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})

class PostDislikeView(View):
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        post.dislikes += 1
        post.save()
        return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})
    
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
        post.likes.add(request.user)
    return JsonResponse({'likes': post.total_likes(), 'dislikes': post.total_dislikes()})

@login_required
def dislike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        post.dislikes.add(request.user)
    return JsonResponse({'likes': post.total_likes(), 'dislikes': post.total_dislikes()})