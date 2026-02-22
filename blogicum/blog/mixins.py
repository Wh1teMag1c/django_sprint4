from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse

from blog.models import Comment, Post

PAGE_PAGINATOR = 10


class CustomListMixin:
    model = Post
    paginate_by = PAGE_PAGINATOR

    def get_queryset(self):
        return (
            Post.objects.select_related(
                'category', 'location', 'author'
            ).annotate(
                comment_count=Count('comments')
            )
        ).order_by('-pub_date')


class PostChangeMixin:
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        """
        При получении объекта не указываем автора.
        Результат сохраняем в переменную.
        Сверяем автора объекта и пользователя из запроса.
        """
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class CommentChangeMixin:
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['post_id']])
