from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator
from .models import Post, Tag, Comment, Reply
from .forms import PostCreateForm, PostEditForm, CommentCreateForm, ReplyCreateForm
from .web_crawler import flickr_crawler

# Create your views here.
def home_view(request, category=None):
    if category:
        posts = Post.objects.filter(tags__slug=category)
        category = get_object_or_404(Tag, slug=category)
    else:    
        posts = Post.objects.all()

    paginator = Paginator(posts, 3)
    page = int(request.GET.get('page', 1))
    try:
        posts = paginator.page(page)
    except:
        return HttpResponse("")

    context = {
        'posts':posts,
        'tag': category,
        'page': page
    }
    if request.htmx:
        return render(request, "snippets/loop_home_posts.html", context)
    
    return render(request, "a_posts/home.html", context)


@login_required
def post_create_view(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # get the url the user enters into the form
            url = form.data['url']
            # print(url)
            try:
                image, title, artist = flickr_crawler(url)
            except:
                return redirect('post_create')

            post.image = image
            post.title = title
            post.artist = artist
            post.author = request.user

            post.save()
            # to save many to many relationships (tags) when besides the post
            form.save_m2m()
            return redirect('home')

    context = {
        'form':form,
    }    

    return render(request, "a_posts/post_create.html", context)


@login_required
def post_delete_view(request, id):
    post = get_object_or_404(Post, pk=id, author=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted')
        return redirect('home')
    
    context = {
        'post': post,
    }
    return render(request, "a_posts/post_delete.html", context )


@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    # Prefill form with data from the fetched post instance
    form = PostEditForm(instance=post)

    if request.method == 'POST':
        # Bind the form with the POST data and the post instance to update it
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, "Post updated!" ) 
            return redirect('home')
        
    context = {
        'post': post,
        'form': form
    }

    return render(request, "a_posts/post_edit.html", context)


def post_page_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    
    commentform = CommentCreateForm()
    replyform = ReplyCreateForm()

    # if request.META.get("HTTP_HX_REQUEST"):
    if request.htmx:
        if 'top' in request.GET:
            # comments = post.comments.filter(likes__isnull=False).distinct()
            comments = post.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        else:
            comments = post.comments.all()

        return render(request, 'snippets/loop_postpage_comments.html', {'comments': comments, 'replyform': replyform})


    context = {
        'post': post,
        'commentform': commentform,
        'replyform': replyform,
    }

    return render(request, "a_posts/post_page.html", context)


@login_required
def comment_sent(request, pk):
    post = get_object_or_404(Post, id=pk)
    replyform = ReplyCreateForm()

    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()

    context = {
        'comment': comment, 
        'post': post, 
        'replyform': replyform
    }

    return render(request, 'snippets/add_comment.html', context)


@login_required
def reply_sent(request, id):
    comment = get_object_or_404(Comment, id=id)
    replyform = ReplyCreateForm()

    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()

    context = {
        'comment': comment, 
        'reply': reply, 
        'replyform': replyform
    }
    return render(request, 'snippets/add_reply.html', context)

@login_required
def comment_delete_view(request, id):
    post = get_object_or_404(Comment, pk=id, author=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Comment deleted')
        return redirect('post', post.parent_post.id )
    
    context = {
        'comment': post,
    }
    return render(request, "a_posts/comment_delete.html", context )


@login_required
def reply_delete_view(request, id):
    reply = get_object_or_404(Reply, pk=id, author=request.user)

    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply deleted')
        return redirect('post', reply.parent_comment.parent_post.id )
    
    context = {
        'reply': reply,
    }
    return render(request, "a_posts/reply_delete.html", context )


def like_toggle(model):
    """
    Decorator to handle like toggling functionality for models.

    Args:
        model: The model for which likes should be toggled.

    Returns:
        A decorator function that wraps the view function.
    """
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            # Retrieve the post or comment object based on the provided pk.
            post = get_object_or_404(model, id=kwargs.get('pk'))

            # Check if the current user has already liked the post/comment.
            user_exists = post.likes.filter(username=request.user.username).exists()

            # Only allow liking if the user is not the author of the post/comment.
            if post.author != request.user:
                if user_exists:
                    # Remove the like if it already exists.
                    post.likes.remove(request.user)
                else:
                    # Add the like if it doesn't exist.
                    post.likes.add(request.user)

            # Call the original view function, passing the updated post object.
            return func(request, post)
        return wrapper
    return inner_func

@login_required
@like_toggle(Post)
def like_post(request, post):
    """
    View function to handle liking a post.

    Args:
        request: The HTTP request object.
        post: The post object to like.

    Returns:
        An HTTP response rendering the likes template.
    """
    return render(request, 'snippets/likes.html', {'post': post})


@login_required
@like_toggle(Comment)
def like_comment(request, post):
    """
    View function to handle liking a comment.

    Args:
        request: The HTTP request object.
        post: The comment object to like.

    Returns:
        An HTTP response rendering the likes template for comments.
    """
    return render(request, 'snippets/likes_comment.html', {'comment': post})


@login_required
@like_toggle(Reply)
def like_reply(request, post):
    """
    View function to handle liking a comment.

    Args:
        request: The HTTP request object.
        post: The comment object to like.

    Returns:
        An HTTP response rendering the likes template for comments.
    """
    return render(request, 'snippets/likes_reply.html', {'reply': post})