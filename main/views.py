from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Post
from .forms import PostForm, SignUpForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def index(request):
    return render(request, 'blog/home.html')

def post_list(request):
    posts = Post.objects.order_by('-created_at')  # Get all posts, ordered by newest
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    # Get the post by primary key (pk)
    post = get_object_or_404(Post, pk=pk)

    # Get all comments related to the post
    comments = post.comments.all()

    # Check if the current user liked the post
    is_liked = post.likes.filter(id=request.user.id).exists()

    # Context to be passed to the template
    context = {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
        'total_likes': post.likes.count(),
    }
    
    return render(request, 'blog/post_detail.html', context)

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # For ManyToMany field (categories)
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', pk=pk)

def new_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect('index')
    else:   
        form = SignUpForm()
    return render(request, 'blog/register.html', {'form': form})

def user_login(request):
    TemplateFile = "blog/login.html"
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to homepage after login
    else:
        form = AuthenticationForm()
    return render(request, TemplateFile, {'form': form})

#logout function
def user_logout(request):
    logout(request)
    return redirect('user_login')  # Redirect to homepage after logout