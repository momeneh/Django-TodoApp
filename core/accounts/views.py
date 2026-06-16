from django.views.generic import FormView
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse_lazy

from rest_framework_simplejwt.tokens import RefreshToken

from datetime import timedelta
from premailer import transform

from .form import RegistrationForm
from .api.v1.utils import EmailThread


def get_tokens_for_user(user):
    token = RefreshToken.for_user(user)
    access = token.access_token
    access.set_exp(lifetime=timedelta(minutes=15))
    return str(access)


class Registeration(FormView):

    template_name = "accounts/register.html"
    form_class = RegistrationForm
    # 'accounts/login/'
    success_url = reverse_lazy("RedirectTodo")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        user = self.object = form.save()
        email = user.email
        token = get_tokens_for_user(user)
        html_template = render_to_string(
            "emails/activation.tpl", {"token": token, "user": user}
        )
        html_inlined = transform(html_template)
        message = EmailMultiAlternatives(
            "Activation Mail", html_inlined, "from@example.cpm", [email]
        )
        message.attach_alternative(html_inlined, "text/html")
        EmailThread(message).start()
        return super().form_valid(form)
