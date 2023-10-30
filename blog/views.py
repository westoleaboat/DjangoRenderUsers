from django.shortcuts import render, get_object_or_404, redirect
from .models import Post

from django.views.generic import ListView

# pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# tags
from taggit.models import Tag
from django.db.models import Count

from plotly.offline import plot
# from utils import get_visual
from .utils import get_visual, generate_visual
import json
from .hn_submissions import hn_articles

from .forms import PostForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 6
    template_name = 'blog/post/list.html'

@login_required
def post_list(request, tag_slug=None):
    # Show all posts to any logged user
    object_list = Post.published.all()

    # Show only user's post to current user
    # object_list = Post.objects.filter(author=request.user).order_by('-created')

    tag = None # optional param that has a None def val.

     # Modify object_list to filter by user or admin
    # if not request.user.is_superuser:
    #     object_list = object_list.filter(author=request.user)

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    # all_tags = Post.objects.values_list('slug', flat=True)
    all_tags = Tag.objects.all()
    # all_tags = Tag.objects.filter(author=request.user)
    # user_tags = Post.objects.filter(author=request.user).values_list('tags__name', flat=True).distinct()

    paginator = Paginator(object_list, 6) # 8 posts in each page
    page = request.GET.get('page')

    # Generate the Plotly figure using the loaded data
    fig2 = generate_visual()

    # plot_html = plot(get_visual(), output_type='div')
    plot_html = plot(fig2, output_type='div')
    
    submission_dicts = hn_articles()
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
        # posts = Post.published.all()

    # Get the image URLs for each post
    post_image_urls = 'https://picsum.photos/900/500'

    context = {
        'page': page,
        'posts': posts,
        'tag': tag,
        'plot_html': plot_html,
        'submission_dicts': submission_dicts,
        'tags': all_tags,
        'post_image_urls': post_image_urls,  # Add this line to pass image URLs
    }
        
    # RETURN OPTIONS ############
    # return render(request, 'blog/post/list.html', {'page':page, 'posts': posts, 'tag': tag, 'plot_html': plot_html, 'submission_dicts': submission_dicts, 'tags': all_tags })
    return render(request, 'blog/post/list2.html', context)
    # return render(request, 'blog/post/psi-blog.html', context)
    # return render(request, 'blog/post/methaphysics-blog.html', context)

@login_required
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                    status='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)

    # Make sure the topic belongs to the current user.
    # if post.author != request.user:
    #     raise Http404
                                    
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post/detail.html', {'post': post, 'similar_posts':similar_posts})



@login_required
def new_post(request):
    if request.method == 'POST':
        # process data
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            if not post.publish:
                # Auto-generate the publish date and time with the current date and time
                post.publish = timezone.now()
            # post.author = request.user  # Assuming you're using authentication.

             # Check if the slug is empty; if it is, generate one
            if not post.slug:
                post.slug = slugify(post.title)

            post.author = request.user

            # Assuming "admin" is the username of your admin user
            # admin_user = User.objects.get(username="admin")
            # post.author = admin_user

            post.save()


             # Process and set tags for the post
            tags_input = form.cleaned_data['tags']

            if isinstance(tags_input, list):
                tags_input = ', '.join(tags_input)  # Convert list to comma-separated string
            
            tags_list = [tag.strip() for tag in tags_input.split(',')]
            post.tags.set(tags_list)

            
            # Use reverse to get the URL for the post_detail view
            url = reverse('blog:post_detail', kwargs={'year': post.publish.year, 'month': post.publish.month, 'day': post.publish.day, 'post': post.slug})
            return redirect(url)
            # return redirect('blog:post_detail', slug=post.slug)  # Replace 'post_detail' with your actual URL pattern name.
    else:
        # blank form
        form = PostForm()

    # Get all existing tags to display in the form
    all_tags = Tag.objects.all()
    return render(request, 'blog/post/new_post.html', {'form': form, 'tags':all_tags})

@login_required
def edit_post(request, year, month, day, post):
    # Retrieve the post object to be edited
    post = get_object_or_404(Post, slug=post, publish__year=year, publish__month=month, publish__day=day)

    # Make sure the topic belongs to the current user.
    if post.author != request.user:
        raise Http404

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            # Redirect to the post's detail page or any other desired page
            return redirect('blog:post_detail', year=year, month=month, day=day, post=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post/edit_post.html', {'form': form, 'post': post})