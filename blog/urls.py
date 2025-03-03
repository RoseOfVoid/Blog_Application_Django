from django.urls import path

from .views import *
from .feeds import LatestPostsFeed


app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('tag/<slug:tag_slug>/', TagListView.as_view(), name='list_by_tag'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', PostDetailView.as_view(), name='detail'),
    path('post/share/<int:post_id>/', post_share, name='share'),
    path('post/comment/<int:post_id>/', post_comment, name='comment'),
    path('feed/', LatestPostsFeed(), name='feed'),
    path('search/', post_search, name='search'),
]