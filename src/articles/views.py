from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import ArticleForm
from .models import Article


def publish_article_view(request, *args, **kwargs):
    """
    If the user is also the author, publish the article.
    If there is no published_date, will set one using timezone.now().
    Redirects to article detail page or 'Page Not Found'.
    """
    # retrieving the article to be published
    articles = Article.objects.filter(slug__iexact=kwargs['slug'])
    article = articles[0]

    # check if the user is the author
    if request.user == article.author:
        article.published = True
        # set a published_date if there is none
        if not article.published_date:
            article.published_date = timezone.now()
        article.save()
        return redirect('home')
    # if the user is not the author raise Page Not Found error
    else:
        raise Http404()


class HomePageView(ListView):
    """
    A list of published articles (from all users) ordered by date, from the newest one to the oldest.
    """
    model = Article
    template_name = 'articles/list.html'

    def get_queryset(self):
        return Article.objects.filter(published=True).order_by('-published_date')


class ArticlesCreateView(LoginRequiredMixin,CreateView):
    """
    Create a new article using the user as the author.
    """
    form_class = ArticleForm
    template_name = 'articles/create.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        return super(ArticlesCreateView, self).form_valid(form)


class ArticlesDetailView(DetailView):
    """
    Article page.
    Uses the template to display different things to author and other users.
    """
    model = Article
    template_name = 'articles/detail.html'


class ArticlesListView(LoginRequiredMixin, ListView):
    """
    A list of user's articles,
    drafts first, and then published,
    ordered by published_date, and then by updated_date,
    from the newest one to the oldest.
    """
    model = Article
    template_name = 'articles/list.html'

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user).order_by('published',
                                                                         '-published_date',
                                                                         '-updated_date')


class ArticlesUpdateView(UserPassesTestMixin, UpdateView):
    """
    Article update view if the user is also the author.
    """
    form_class = ArticleForm
    template_name = 'articles/update.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_queryset(self):
        return Article.objects.all()


class ArticlesDeleteView(UserPassesTestMixin, DeleteView):
    form_class = ArticleForm
    template_name = 'articles/delete.html'
    success_url = reverse_lazy('articles:list')

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_queryset(self):
        return Article.objects.all()
