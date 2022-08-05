from django import template
from articles.models import Article


register = template.Library()


@register.simple_tag()
def get_all_articles():
    return Article.objects.all()
