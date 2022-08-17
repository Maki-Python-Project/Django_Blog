import logging
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.db.models import F, Q
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Count
from .forms import CommentForm
from .models import Comment, Article, Category
from users.models import CustomUser


logger = logging.getLogger(__name__)


class CategoryUserList:
    def get_categories(self):
        return Category.objects.all()

    def get_authors(self):
        return CustomUser.objects.all()


class ArticleListView(CategoryUserList, ListView):
    model = Article
    template_name = 'articles/article_list.html'
    queryset = model.objects.filter(draft=False).select_related('author')


# def popular(request):
#     queryset = Article.objects.filter(draft=False).order_by('-views')
#     return render(
#         request, 'articles/article_popular.html', {'popular_articles': queryset}
#     )


class DraftArticleListView(ListView):
    model = Article
    template_name = 'articles/article_draft.html'


class ArticleAddComment(View):
    def post(self, request, pk):
        post = Article.objects.get(id=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.customer = request.user
            comment.text = form.cleaned_data['text']
            comment.article = post
            comment.save()
        else:
            error_string = ' '.join(
                [' '.join(x for x in el) for el in list(form.errors.values())]
            )
            print(error_string)
            messages.success(request, f'Errors: {error_string}')

        return redirect(post.get_absolute_url())


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'articles/article_detail.html'

    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        queryset = Article.objects.filter(pk=pk)
        queryset.update(
            views=F('views') + 1
        )

        return queryset


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ['title', 'body']
    template_name = 'articles/article_edit.html'
    login_url = 'login'

    def get_object(self, queryset=None):
        obj = super(ArticleUpdateView, self).get_object(queryset)
        if self.request.user.is_superuser:
            return obj
        if obj.author != self.request.user:
            raise ValueError(
                "You are not the author of this post, so you cannot edit it"
            )
        return obj


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'articles/article_delete.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login'

    def get_object(self, queryset=None):
        obj = super(ArticleDeleteView, self).get_object(queryset)
        if self.request.user.is_superuser:
            return obj
        if obj.author != self.request.user:
            raise ValueError(
                "You are not the author of this post, so you cannot delete it"
            )
        return obj


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'articles/article_new.html'
    fields = ['title', 'body', 'category']
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def hello_reader(request):
    logger.warning(
        'Endpoint articles/logger was accessed at '+str(datetime.datetime.now())+' hours!'
    )

    return HttpResponse("<h2>Custom logger</h2>")


class FilterArticleView(CategoryUserList, ListView):
    def get_queryset(self):
        queryset = Article.objects.filter(
            Q(category__id__in=self.request.GET.getlist("category")) |
            Q(author__id__in=self.request.GET.getlist("author"))
        )

        return queryset


class CategoryView(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = 'articles/category_list.html'


class CategoryDetailView(ListView):
    model = Category
    template_name = 'articles/category_detail.html'

    def get_queryset(self):
        category_article = Category.objects.get(id=self.kwargs['pk'])
        queryset = category_article.articles.all().prefetch_related('author')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_category'] = category_article = Category.objects.get(
            id=self.kwargs['pk']
        )
        context['count_article'] = list(
            category_article.articles.aggregate(
                Count('category_id')
            ).values())[0]
        return context
