import logging
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import CommentForm
from django.shortcuts import redirect
from .models import Comment, Article


logger = logging.getLogger(__name__)


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    queryset = model.objects.filter(draft=False)


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
        return redirect(post.get_absolute_url())


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'articles/article_detail.html'


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
    fields = ['title', 'body']
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def hello_reader(request):
    logger.warning(
        'Endpoint articles/logger was accessed at '+str(datetime.datetime.now())+' hours!'
    )
    return HttpResponse("<h2>Custom logger</h2>")
