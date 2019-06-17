from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.safestring import mark_safe


class Article(models.Model):
    author          = models.ForeignKey(User, on_delete=models.CASCADE)

    title           = models.CharField(max_length=120, unique=True)
    content         = models.TextField()

    created_date    = models.DateTimeField(auto_now_add=True)
    updated_date    = models.DateTimeField(auto_now=True)
    published_date  = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)

    slug            = models.SlugField(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'slug': self.slug})

    def get_html(self):
        return mark_safe(self.content)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        return super(Article, self).save(*args, **kwargs)

    class Meta:
        ordering = ['title']
