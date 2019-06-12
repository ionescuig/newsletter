from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import SignUpForm
from .models import Profile


def activate(request, code):
    try:
        profile = Profile.objects.get(activation_key=code)
    except:
        profile = None
    if profile is not None:
        profile.user.is_active = True
        profile.activation_key = None
        profile.activated = True
        profile.user.save()
        return redirect('login')
    else:
        return redirect('profiles:account_invalid')


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        email_address = form['email'].value()
        if form.is_valid() and not User.objects.filter(email__exact=email_address):
            user = form.save()
            user.is_active = False
            user.save()
            user.refresh_from_db()  # load the profile instance created by the signal

            # send activation email
            base_url = "{0}://{1}".format(request.scheme, request.get_host())
            user.profile.send_activation_mail(base_url)

            return redirect('profiles:email_sent')
    else:
        form = SignUpForm()
    return render(request, 'profiles/signup.html', {'form': form})


class EmailSentView(TemplateView):
    template_name = 'profiles/email_sent.html'


class AccountInvalidView(TemplateView):
    template_name = 'profiles/account_invalid.html'


class ProfileUpdateView(UpdateView):
    model = User
    template_name = 'profiles/profile_update.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = '/'
