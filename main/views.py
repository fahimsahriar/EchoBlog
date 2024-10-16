from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'blog/home.html')


#@login_required
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