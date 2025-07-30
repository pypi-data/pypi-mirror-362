import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from tom_registration.registration_flows.open.forms import OpenRegistrationForm
from tom_registration import __version__

logger = logging.getLogger(__name__)


class OpenRegistrationView(CreateView):
    """
    View for registering in the open registration flow. This view creates the user, adds them to the public group, and
    immediately logs them in.
    """
    template_name = 'tom_registration/register_user.html'
    success_url = reverse_lazy(settings.TOM_REGISTRATION.get('REGISTRATION_REDIRECT_PATTERN', 'home'))
    form_class = OpenRegistrationForm
    extra_context = {'version': __version__}

    def form_valid(self, form):
        super().form_valid(form)
        group, _ = Group.objects.get_or_create(name='Public')
        group.user_set.add(self.object)
        group.save()

        messages.info(self.request, 'Registration was successful!')
        if isinstance(self.object, User):
            try:
                login(self.request, self.object,
                      backend=settings.TOM_REGISTRATION.get('REGISTRATION_AUTHENTICATION_BACKEND'))
            except ValueError as ve:
                logger.error(f'Unable to log in newly registered user: {ve}')

        return redirect(self.get_success_url())
