"""newsletter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from articles.views import HomePageView

handler403 = 'profiles.views.handler403'
handler404 = 'profiles.views.handler404'
handler500 = 'profiles.views.handler500'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('articles/', include(('articles.urls', 'articles'), namespace='articles')),
    path('summernote/', include('django_summernote.urls')),
    path('profile/', include(('profiles.urls', 'profiles'), namespace='profiles')),
    path('profile/password_reset/', auth_views.PasswordResetView.as_view(
        html_email_template_name='registration/password_reset_email.html')),
    path('profile/', include('django.contrib.auth.urls')),
]
