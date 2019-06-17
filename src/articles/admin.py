from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Article


class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', )
    fields = ['title', 'author', 'published_date', 'updated_date', 'created_date', 'content']
    readonly_fields = ('author', 'published_date', 'updated_date', 'created_date')
    list_display = ['title', 'author', 'published_date']
    list_filter = ['author', 'title']
    search_fields = ['title', 'author__username']


admin.site.register(Article, ArticleAdmin)

