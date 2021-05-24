from django.views import generic
from django.urls import reverse
from .forms import SubscribedUserForm
from .models import SubscribedUser

# Create your views here.

class SubscribedUserCreateView(generic.CreateView):
    model = SubscribedUser
    form_class = SubscribedUserForm
    template_name = 'mail-magazine/form.html'

    def get_success_url(self):
        return reverse('mailMagazine:complete')

class SubscribedUserCreateCompleteView(generic.TemplateView):
    template_name = 'mail-magazine/complete.html'