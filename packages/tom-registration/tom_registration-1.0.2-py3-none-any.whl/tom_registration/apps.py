from django.apps import AppConfig
from django.urls import path, include
from django.conf import settings


class TomRegistrationConfig(AppConfig):
    name = 'tom_registration'

    def include_url_paths(self):
        """
        Integration point for adding URL patterns to the Tom Common URL configuration.
        This method should return a list of URL patterns to be included in the main URL configuration.
        """
        registration_strategy = settings.TOM_REGISTRATION['REGISTRATION_STRATEGY']
        urlpatterns = [
            path('', include(f'tom_registration.registration_flows.{registration_strategy}.urls',
                             namespace='registration')),
        ]
        return urlpatterns

    def nav_items(self):
        """
        Integration point for adding items to the navbar.
        This method should return a list of partial templates to be included in the navbar.
        """
        return [{'partial': 'tom_registration/partials/register_button.html', 'position': 'right'}]

    def user_lists(self):
        """
        Integration point for adding items to the user list page.

        This method should return a list of dictionaries that include a `partial` key pointing to the path of the html
        user_list partial. The `context` key should point to the dot separated string path to the templatetag that will
        return a dictionary containing new context for the accompanying partial.
        Typically, this partial will be a bootstrap table displaying some app specific user list or similar.

        """
        if settings.TOM_REGISTRATION['REGISTRATION_STRATEGY'] == 'approval_required':
            return [{'partial': 'tom_registration/partials/pending_users.html',
                     'context': 'tom_registration.templatetags.registration_extras.pending_users'}]
        else:
            return []
