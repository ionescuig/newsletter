from django.urls import include, path

from .views import AccountInvalidView, activate, EmailSentView, ProfileUpdateView, signup_view

urlpatterns = [
    path('invalid-account', AccountInvalidView.as_view(), name='account_invalid'),
    path('activate/<str:code>', activate, name='activate'),
    path('email-sent', EmailSentView.as_view(), name='email_sent'),
    path('update/<int:pk>', ProfileUpdateView.as_view(), name='profile_update'),
    path('signup', signup_view, name='signup'),
]
