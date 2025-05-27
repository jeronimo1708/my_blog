# blog_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment # Import Comment model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from resume_app.data import RESUME_DATA
from .forms import CommentForm # Import the new CommentForm
from django.contrib.auth.decorators import login_required # <--- ADD THIS IMPORT
from django.views.decorators.http import require_POST # <--- ADD THIS IMPORT (optional but good practice)

def post_list(request):
    object_list = Post.objects.filter(status='published')
    paginator = Paginator(object_list, 5) # 5 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    # Pass resume data for the sidebar in post_list
    from resume_app.data import RESUME_DATA # Import RESUME_DATA
    context = {
        'page': page,
        'posts': posts,
        # 'resume': RESUME_DATA # Pass resume data
    }
    return render(request, 'blog_app/post_list.html', context)

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    
    # Retrieve all active comments for this post
    comments = post.comments.filter(active=True) # Use the related_name 'comments'
    # Initialize a new comment form
    new_comment = None
    comment_form = None # Initialize to None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST) # Populate form with POST data
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            # Redirect to the same page to prevent resubmission on refresh
            # We redirect to the post_detail URL, ensuring URL is canonical
            return redirect(post.get_absolute_url())
        else:
            # If form is not valid, the invalid form will be passed back to the template
            pass # Keep the invalid form with errors to display
    else:
        # Initial request (GET)
        comment_form = CommentForm() # Create an empty form

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form, # Pass the form to the template
        'resume': RESUME_DATA # Pass resume data for the navbar
    }
    return render(request, 'blog_app/post_detail.html', context)

@login_required # Ensures only logged-in users can access this view
@require_POST # Ensures this view only accepts POST requests (good for security)
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id) # Get the post by its ID
    
    # Toggle the like status
    if request.user in post.likers.all():
        post.likers.remove(request.user) # User already liked, so remove the like
    else:
        post.likers.add(request.user) # User hasn't liked, so add the like

    # Redirect back to the post detail page
    return redirect(post.get_absolute_url())