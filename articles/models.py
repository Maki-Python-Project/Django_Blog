from django.conf import settings
from django.db import models
from django.urls import reverse


class DraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(draft=True)


class Category(models.Model):
    name = models.CharField(max_length=150)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    category = models.ForeignKey(
        Category, related_name='articles', on_delete=models.SET_NULL, null=True
    )
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    views = models.IntegerField(default=0, null=True, blank=True)
    draft = models.BooleanField(default=False)
    objects = models.Manager()
    draft_true = DraftManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])


class Comment(models.Model):
    text = models.CharField(max_length=200)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments', null=True
    )

    def __str__(self) -> str:
        return f'{self.text}; author: {self.customer}'
