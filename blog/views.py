from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag


class PostListView(ListView):
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

    def get_queryset(self, *args, **kwargs):
        return Post.published.all()


class TagListView(PostListView):

    def get_queryset(self, *args, **kwargs):
        return Post.published.filter(tags__slug=self.kwargs.get('tag_slug'))


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=slug, publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {'post': post, 'comments': comments, 'form': form}
    return render(request, 'blog/post/detail.html', context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = (f"{cd['name']} ({cd['email']}) "
            f"recommends you read {post.title}")
            message = (f"Read {post.title} at http://127.0.0.1:8000{post.get_absolute_url()}\n\n"
                       f"{cd['name']}\'s coments: {cd['comments']}")
            send_mail(subject=subject, message=message, from_email=None, recipient_list=[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {'post': post, 'form': form, 'sent': sent}
    return render(request, 'blog/post/share.html', context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {'post': post, 'form': form, 'comment': comment}
    return render(request, 'blog/post/comment.html', context)