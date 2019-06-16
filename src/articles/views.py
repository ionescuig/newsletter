from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.shortcuts import render

from .forms import ArticleForm
from .models import Article


class HomePageView(ListView):
    model = Article
    template_name = 'articles/list.html'

    def get_queryset(self):
        return Article.objects.filter(published=True).order_by('-published_date')


class ArticlesCreateView(LoginRequiredMixin,CreateView):
    form_class = ArticleForm
    template_name = 'articles/create.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        return super(ArticlesCreateView, self).form_valid(form)


class ArticlesDetailView(DetailView):
    model = Article
    template_name = 'articles/detail.html'


class ArticlesListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'articles/list.html'

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user).order_by('published', '-published_date')


class ArticlesUpdateView(UserPassesTestMixin, UpdateView):
    form_class = ArticleForm
    template_name = 'articles/update.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_queryset(self):
        return Article.objects.all()

