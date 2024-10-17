from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Post, Comment
from .forms import PostForm, SignUpForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    posts = Post.objects.order_by('-created_at')  # Get all posts, ordered by newest

    paginator = Paginator(posts, 6)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    posts_obj = paginator.get_page(page_number)

    return render(request, 'blog/home.html', {'posts': posts_obj})

@login_required
def post_list(request):
    posts = Post.objects.order_by('-created_at')  # Get all posts, ordered by newest

    paginator = Paginator(posts, 5)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    posts_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'posts': posts_obj})

@login_required
def post_detail(request, pk):
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            post = get_object_or_404(Post, id=pk)
            comment = Comment.objects.create(post=post, author=request.user, content=content)
            return redirect('post_detail', pk=pk)
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

@login_required
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

@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id = post_id)
    # Check if the logged-in user is the author of the post
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            print("Hi")
            print(post.author)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

#Delete Post
@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id = post_id)
    # Check if the logged-in user is the author of the post
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    if request.method == 'POST':
        post.delete()
        return redirect("index")
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_delete.html', {'post': post})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Toggle the user's like status
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Unlike
        liked = False
    else:
        post.likes.add(request.user)  # Like
        liked = True

    return JsonResponse({
        'liked': liked,
        'like_count': post.likes.count(),
    })

#User registration
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

#Custom user login
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

#User profile view
@login_required
def user_profile(request, username):
    # Get the user by username
    user = get_object_or_404(User, username=username)

    # Get posts authored by the user
    user_posts = Post.objects.filter(author=user).order_by('-created_at')

    # Pagination (5 posts per page)
    paginator = Paginator(user_posts, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    context = {
        'user_profile': user,
        'posts': posts,
    }

    return render(request, 'blog/user_profile.html', context)