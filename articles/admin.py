from django.contrib import admin
from . import models


class CommentInLine(admin.TabularInline):
    model = models.Comment
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'date', 'author')
    list_filter = ('title', 'author')
    search_fields = ('title', 'date')
    save_on_top = True
    inlines = [
        CommentInLine,
    ]


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Comment)
