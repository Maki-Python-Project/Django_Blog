from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('categories/', views.CategoryView.as_view(), name='article_popular'),
    path('filter/', views.FilterArticleView.as_view(), name='filter'),
    path('<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_edit'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('new/', views.ArticleCreateView.as_view(), name='article_new'),
    path('<int:pk>/comment/', views.ArticleAddComment.as_view(), name='article_comment'),
    path('logger/', views.hello_reader, name='hello_reader'),
    path('draft/', cache_page(30)(views.DraftArticleListView.as_view()), name='article_draft'),
]
