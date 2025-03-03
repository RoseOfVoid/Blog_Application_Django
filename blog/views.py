from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


class PostListView(ListView):
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context


class TagListView(PostListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        context['tag'] = tag
        context['posts'] = Post.published.filter(tags__in=[tag])
        return context



class PostDetailView(DetailView):

    model = Post
    template_name = 'blog/post/detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=self.kwargs['slug'], publish__year=self.kwargs['year'],
                                 publish__month=self.kwargs['month'], publish__day=self.kwargs['day'])
        comments = post.comments.filter(active=True)
        post_tag_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tag_ids).exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

        context['comments'] = comments
        context['post'] = post
        context['form'] = CommentForm()
        context['similar_posts'] = similar_posts
        return context


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


def post_search(request):
    form = SearchForm()
    query = None
    result = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            result = (Post.published.annotate(search=search_vector, rank=SearchRank(search_vector,search_query)).filter(rank__gte=0.3).order_by('-rank'))


    context = {
        'form': form,
        'query': query,
        'result': result
    }
    return render(request, 'blog/post/search.html', context=context)

