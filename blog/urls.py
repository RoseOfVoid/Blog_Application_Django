from django.urls import path

from .views import *

app_name = 'blog'
urlpatterns = [
    path('', post_list, name='list'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', post_detail, name='detail'),
]