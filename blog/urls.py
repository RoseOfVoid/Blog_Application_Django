from django.urls import path

from .views import *

app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', post_detail, name='detail'),
    path('post/share/<int:post_id>/', post_share, name='share'),
]