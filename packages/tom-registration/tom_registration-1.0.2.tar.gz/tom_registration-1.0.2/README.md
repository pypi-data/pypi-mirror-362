[![pypi](https://img.shields.io/pypi/v/tom-registration.svg)](https://pypi.python.org/pypi/tom-registration)
[![run-tests](https://github.com/TOMToolkit/tom_registration/actions/workflows/run-tests.yml/badge.svg)](https://github.com/TOMToolkit/tom_registration/actions/workflows/run-tests.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/96d28f95266144f7afc7d118050b24ba)](https://www.codacy.com/gh/TOMToolkit/tom_registration/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=TOMToolkit/tom_registration&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/TOMToolkit/tom_registration/badge.svg?branch=main)](https://coveralls.io/github/TOMToolkit/tom_registration?branch=main)

# TOM Registration

This reusable TOM Toolkit app provides support for two user registration flows in the TOM Toolkit.

The two registration flows are as follows:

 1. Open Registration - In this flow, the user fills in a registration form and is immediately able to access the TOM and see all public data.

 2. Approval Registration - In this flow, the user fills in a registration form, and is inactive until an administrator reviews and approves their registration.

## Installation

 1. Install the package into your TOM environment:
   ```bash
   pip install tom-registration
   ```

 2. In your project `settings.py`, add `tom_registration` to your `INSTALLED_APPS` setting:

    ```python
    INSTALLED_APPS = [
        ...
        'tom_registration',
    ]
    ```

    And add the follow setting, with appropriate values for your use case:

    ```python
    TOM_REGISTRATION = {
        'REGISTRATION_AUTHENTICATION_BACKEND': 'django.contrib.auth.backends.ModelBackend',
        'REGISTRATION_REDIRECT_PATTERN': 'home',
        'REGISTRATION_STRATEGY': 'open',  # ['open', 'approval_required']
        'SEND_APPROVAL_EMAILS': True,  # Optional email behavior if `REGISTRATION_STRATEGY = 'approval_required'`, default is False
        'APPROVAL_SUBJECT': f'Your {TOM_NAME} registration has been approved!',  # Optional subject line of approval email, (Default Shown)
        'APPROVAL_MESSAGE': f'Your {TOM_NAME} registration has been approved. You can log in <a href="mytom.com/login">here</a>.'  # Optional html-enabled body for approval email, (Default Shown)
    }
    ```

    To prevent logged-in users from accessing the registration page, add `RedirectAuthenticatedUsersFromRegisterMiddleware` to the `MIDDLEWARE` settings:

    ```python
    MIDDLEWARE = [
        ...
        'tom_common.middleware.AuthStrategyMiddleware',
        'tom_registration.middleware.RedirectAuthenticatedUsersFromRegisterMiddleware',
    ]
    ```
 
 3. If you're using approval registration and you would like a message informing the user that their account is pending approval if they try to log in prior to approval, you'll need to make the following changes:

     First, in your `settings.py`, set the first item of your `AUTHENTICATION_BACKENDS`:

     ```python
     AUTHENTICATION_BACKENDS = (
         'django.contrib.auth.backends.AllowAllUsersModelBackend',
         'guardian.backends.ObjectPermissionBackend'
     )
     ```

     Then, change the value of `REGISTRATION_AUTHENTICATION_BACKEND` in the `TOM_REGISTRATION` setting that was just created:

     ```python
     TOM_REGISTRATION = {
         'REGISTRATION_AUTHENTICATION_BACKEND': 'django.contrib.auth.backends.AllowAllUsersModelBackend',
         ...
     }
     ```

## Email

In the approval required registration flow, there is available behavior to send basic emails notifying moderators
of a registration request, and notifying users of registration approval. Administrators are determined by the
[Django MANAGERS setting](https://docs.djangoproject.com/en/stable/ref/settings/#managers). 
Email behavior can be enabled or disabled with `SEND_APPROVAL_EMAILS`.

The configuration of an email backend is a topic covered in depth by the 
[Django docs](http://docs.djangoproject.com/en/stable/topics/email/#smtp-backend). 
There are a number of required settings that will need to be added.
An example of how the most important settings should look something like the following:

```python
    MANAGERS = [('Manager1', 'manager@my_tom.com')]  # List of managers who should receive registration emails
    EMAIL_SUBJECT_PREFIX = f'[{TOM_NAME}]'  # Optional prefix for all approval requests to managers
    EMAIL_HOST = 'smtp.gmail.com'   # SMTP server for sending emails (this example is for gmail)
    EMAIL_PORT = 587  # Port for the SMTP server
    EMAIL_HOST_USER = 'my_tom@gmail.com'  # Email address for the account sending emails
    EMAIL_HOST_PASSWORD = '******************'  # Password for the account sending emails (app password for gmail)
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = True  # this is needed for gmail, other services may vary
    EMAIL_USE_SSL = False  # this is needed for gmail, other services may vary
    SERVER_EMAIL = "my_tom@email.com"  # Email address used as the "from" address if EMAIL_HOST_USER is not needed
```

**Note if using gmail:** the `EMAIL_HOST_PASSWORD` above is not the account email password associated with `EMAIL_HOST_USER`,
but an app password generated by the account owner. This can be generated from the account settings page by searching for "app passwords".


## Running the tests

In order to run the tests, run the following in your virtualenv:

```bash
    python tom_registration/tests/run_tests.py
```

For options see
```bash
    python tom_registration/tests/run_tests.py --help
```

