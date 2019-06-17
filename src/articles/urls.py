from django.urls import path

from .views import ArticlesCreateView, ArticlesDeleteView, ArticlesDetailView,\
    ArticlesListView, ArticlesUpdateView, publish_article_view

urlpatterns = [
    path('all', ArticlesListView.as_view(), name='list'),
    path('new', ArticlesCreateView.as_view(), name='create'),
    path('<str:slug>/delete', ArticlesDeleteView.as_view(), name='delete'),
    path('<str:slug>/publish', publish_article_view, name='publish'),
    path('<str:slug>/update', ArticlesUpdateView.as_view(), name='update'),
    path('<str:slug>', ArticlesDetailView.as_view(), name='detail'),
]
