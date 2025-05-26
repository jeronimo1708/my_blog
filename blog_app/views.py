# blog_app/views.py
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment # Import Comment model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
        'resume': RESUME_DATA # Pass resume data
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

    # Pass resume data for the sidebar in post_detail
    from resume_app.data import RESUME_DATA # Import RESUME_DATA
    context = {
        'post': post,
        'comments': comments,
        'resume': RESUME_DATA # Pass resume data
    }
    return render(request, 'blog_app/post_detail.html', context)