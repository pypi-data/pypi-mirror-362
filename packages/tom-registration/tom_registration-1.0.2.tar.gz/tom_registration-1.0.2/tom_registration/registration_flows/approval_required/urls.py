from django.contrib.auth.views import LoginView
from django.urls import path

from tom_registration.registration_flows.approval_required.forms import ApprovalAuthenticationForm
from tom_registration.registration_flows.approval_required.views import ApprovalRegistrationView, UserApprovalView

app_name = 'tom_registration'


urlpatterns = [
    path('accounts/login/', LoginView.as_view(authentication_form=ApprovalAuthenticationForm), name='login'),
    path('accounts/register/', ApprovalRegistrationView.as_view(), name='register'),
    path('accounts/approve/<int:pk>/', UserApprovalView.as_view(), name='approve')
]
