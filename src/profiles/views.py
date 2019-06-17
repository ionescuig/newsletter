from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, render_to_response
from django.views.generic import TemplateView, UpdateView


from .forms import SignUpForm
from .models import Profile


# custom errors 403, 404, 500
def handler403(request, exception, template_name="403.html"):
    response = render_to_response("403.html")
    response.status_code = 403
    return response


def handler404(request, exception, template_name="404.html"):
    response = render_to_response("404.html")
    response.status_code = 404
    return response


def handler500(request, template_name="404.html"):
    response = render_to_response("500.html")
    response.status_code = 500
    return response


def activate(request, code):
    """
    Function triggered from the user email activation link.
    If the activation key is valid activates the user and profile.
    """
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


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Only the user's profile can be modified.
    """
    model = User
    template_name = 'profiles/profile_update.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user
