import logging
from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.core.mail import mail_managers, send_mail
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy

from tom_common.mixins import SuperuserRequiredMixin
from tom_registration.registration_flows.approval_required.forms import ApproveUserForm
from tom_registration.registration_flows.approval_required.forms import RegistrationApprovalForm
from tom_registration import __version__

logger = logging.getLogger(__name__)


# TODO: Add post-approval hooks that actually handle the sending of email
class ApprovalRegistrationView(CreateView):
    """
    View for handling registration requests in the approval required registration flow. This flow creates users but sets
    them as inactive, requiring administrator approval in order to log in. Upon registration, an email is sent to the
    administrators of the TOM informing them of the request.
    """
    template_name = 'tom_registration/register_user.html'
    success_url = reverse_lazy(settings.TOM_REGISTRATION.get('REGISTRATION_REDIRECT_PATTERN', ''))
    form_class = RegistrationApprovalForm
    extra_context = {'version': __version__}

    def form_valid(self, form):
        super().form_valid(form)
        group, _ = Group.objects.get_or_create(name='Public')
        group.user_set.add(self.object)
        group.save()

        messages.info(self.request, 'Your request to register has been submitted to the administrators.')

        if settings.TOM_REGISTRATION.get('SEND_APPROVAL_EMAILS'):
            try:
                current_domain = Site.objects.get_current().domain
                link_to_user_list = f'https://{current_domain}{reverse("user-list")}'
                mail_managers(
                    subject=f'Registration Request from {self.object.first_name} {self.object.last_name}',
                    message='',  # leave this blank in favor of html_message
                    fail_silently=False,
                    html_message=f'{self.object.first_name} {self.object.last_name} '
                                 f'has requested to register in your TOM. Please approve or delete this user'
                                 f' <a href="{link_to_user_list}">here</a>.',
                )
            except (SMTPException, ConnectionRefusedError) as error:
                logger.error(f'Unable to send email: {error}')

        return redirect(self.get_success_url())


class UserApprovalView(SuperuserRequiredMixin, UpdateView):
    """
    View for approving (activating) pending (inactive) users in the approval required registration flow. Upon approval,
    an email is sent to the user informing them of the registration approval.
    """
    model = User
    template_name = 'tom_registration/approve_user.html'
    success_url = reverse_lazy('user-list')
    form_class = ApproveUserForm

    def form_valid(self, form):
        response = super().form_valid(form)

        if settings.TOM_REGISTRATION.get('SEND_APPROVAL_EMAILS'):
            try:
                current_domain = Site.objects.get_current().domain
                link_to_login = f'https://{current_domain}{reverse("login")}'
                send_mail(
                    subject=settings.TOM_REGISTRATION.get('APPROVAL_SUBJECT',
                                                          f'Your {settings.TOM_NAME} '
                                                          f'registration has been approved!'),
                    message='',  # leave this blank in favor of html_message
                    from_email=settings.SERVER_EMAIL,
                    recipient_list=[self.object.email],
                    html_message=settings.TOM_REGISTRATION.get(
                        'APPROVAL_MESSAGE',
                        f'Your {settings.TOM_NAME} registration has been approved. '
                        f'You can log in <a href="{link_to_login}">here</a>.'
                    ),
                    fail_silently=False)
            except (SMTPException, ConnectionRefusedError) as error:
                logger.error(f'Unable to send email: {error}')

        return response
