from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView

from users.forms import CustomUserCreationForm


class RegisterView(CreateView):
    model = get_user_model()
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('landing')
