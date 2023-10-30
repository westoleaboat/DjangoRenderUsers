from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# tags
from taggit.managers import TaggableManager
# markdown
from markdownx.models import MarkdownxField
# slug
from django.utils.text import slugify
# users
# from django.contrib.auth.models import User

# Create your models here.


# def upload_to(instance, filename):
#     return f'media/posts/{instance.slug}/{filename}'


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = ( ('draft', 'Draft'), ('published', 'Published'),)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    # body = models.TextField()
    image_url = models.URLField(default='https://picsum.photos/900/500')
    body = MarkdownxField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager() # the default manager.
    published = PublishedManager() # Our custom manager.
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        # Generate the slug from the title if it's not provided
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)
    

    def get_absolute_url(self):
        return reverse("blog:post_detail", 
                        args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    



    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title