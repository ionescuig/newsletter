from django.urls import path

from .views import ArticlesCreateView, ArticlesDetailView, ArticlesListView, ArticlesUpdateView

urlpatterns = [
    path('all', ArticlesListView.as_view(), name='list'),
    path('new', ArticlesCreateView.as_view(), name='create'),
    path('update/<str:slug>', ArticlesUpdateView.as_view(), name='update'),
    path('<str:slug>', ArticlesDetailView.as_view(), name='detail'),
]
