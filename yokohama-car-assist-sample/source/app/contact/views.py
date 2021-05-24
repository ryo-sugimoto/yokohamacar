from django.views import generic
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .forms import ContactForm
from .models import Contact
import environ

# Load .env
env = environ.Env()
env.read_env('.env')

CONFIRM_MAIL_SUBJECT = 'お問い合わせが完了いたしました。'

# Create your views here.

class ContactCreateView(generic.CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact/form.html'

    def get_success_url(self):
        return reverse('contact:complete')

    def form_valid(self, form):
        post_data = self.request.POST
        message = post_data.get('content')
        context = {
            'name': post_data.get('name'),
            'message': message,
        }
        # 確認メールの送信
        send_mail(
            CONFIRM_MAIL_SUBJECT,
            message,
            env('EMAIL_HOST_USER'),
            [post_data.get('mail_address')],
            html_message=render_to_string('contact/confirm-mail.html', context))
        return super().form_valid(form)

class ContactCreateCompleteView(generic.TemplateView):
    template_name = 'contact/complete.html'