from django import template
from articles.models import Article


register = template.Library()


@register.simple_tag()
def get_all_draft_articles():
    return Article.draft_true.all()
