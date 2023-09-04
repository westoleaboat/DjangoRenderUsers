from django import template
from ..models import Post
from django.utils.safestring import mark_safe
# import markdown
import markdownx
import re

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {"latest_posts": latest_posts}

@register.filter(name='markdownx')
def markdown_format(text):
    return mark_safe(markdownx.utils.markdownify(text))


@register.filter(name='remove_images')
def remove_images(value):
    # Remove image HTML tags
    return re.sub(r'<img.*?alt="image".*?>', '', value)