from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
# from django.views.generic import ListView - это если через класс
from django.views.decorators.http import require_POST
from django.conf import settings
from django.db.models import Count
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .models import Post    # нету Comment - потому-что коменты через форму
from .forms import EmailPostForm, CommentForm, SearchForm



def post_list(request, tag_slug=None):
    post_list = Post.published.all()

    # собираем теги
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags=tag)
    else:
        tag = None
    
    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context={'posts': posts, "tag": tag}
    return render(request,
                  template_name='blog/post/list.html',
                  context=context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # Список активных комментариев к этому посту
    comments = post.comments.filter(active=True)
    # Форма для комментирования пользователями
    form = CommentForm()
    # Список схожих постов
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)
    similar_posts = similar_posts.exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags"))
    similar_posts = similar_posts.order_by("-same_tags", "-publish")[:4]

    context = {'post': post,
               'comments': comments,
               'form': form,
               "similar_posts": similar_posts}
    return render(request,
                  template_name='blog/post/detail.html',
                  context=context)

"""
class PostListView(ListView):
    "Альтернативное представление списка постов"
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"
"""

def post_share(request, post_id):
    # Извлечь пост по его идентификатору id
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s ({cd['email']}) comments: {cd['comments']}"
            send_mail(subject, message, settings.EMAIL_HOST_USER,
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    context = {'post': post, 'form': form, 'sent': sent}
    return render(request,
                  template_name='blog/post/share.html',
                  context=context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.post = post
        # Сохранить комментарий в базе данных
        comment.save()
    else:
        comment = None
    
    context = {'post': post, 'form': form, 'comment': comment}
    return render(request,
                  template_name='blog/post/comment.html',
                  context=context)


def post_search(request):
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_vector = SearchVector("title", "body", config="russian")
            search_query = SearchQuery(query, config="russian")
            results = Post.published.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by("-rank")
    else:
        form = SearchForm()
        query = None
        results = []
    
    context = {"form": form, "query": query, "results": results}
    return render(request,
                  template_name="blog/post/search.html",
                  context=context)
