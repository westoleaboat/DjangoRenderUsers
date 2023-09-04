from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    # Index Page, list of all posts
    path('', views.post_list, name='post_list'),
    # path('', views.PostListView.as_view(), name='post_list'),
    # Single Post Page
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post_detail'), 
    # list by tag
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # Create a new post
    path('new_post/', views.new_post, name='new_post'),
    # Edit a post
    path('<int:year>/<int:month>/<int:day>/<slug:post>/edit/', views.edit_post, name="edit_post"),

    
]