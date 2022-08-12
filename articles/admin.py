from django.contrib import admin
from . import models


class CommentInLine(admin.TabularInline):
    model = models.Comment
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'date', 'author', 'views')
    list_filter = ('title', 'author', 'category')
    search_fields = ('title', 'date')
    save_on_top = True
    inlines = [
        CommentInLine,
    ]


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Comment)
admin.site.register(models.Category)
