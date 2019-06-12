from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse
from django.template.loader import render_to_string

from .utils import code_generator


class Profile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_key  = models.CharField(max_length=120, blank=True, null=True)
    activated       = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def send_activation_mail(self, base_url):
        if not self.activated:
            self.activation_key = code_generator()
            self.save()
            activate_url = base_url + reverse('profiles:activate', kwargs={'code': self.activation_key})
            context = {'user': self.user, 'activate_url': activate_url}
            html_content = render_to_string('profiles/html_message.html', context)
            subject = 'Activate your account'
            from_email = settings.DEFAULT_FROM_EMAIL
            message = 'Activate your account here'
            recipient_list = [self.user.email]

            sent_mail = send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False,
                html_message=html_content
            )
        return sent_mail

    class Meta:
        ordering = ['-activated', 'user', ]


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
