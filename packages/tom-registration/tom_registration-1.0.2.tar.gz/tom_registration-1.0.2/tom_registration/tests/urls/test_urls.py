from django.urls import include, path

app_name = 'tom_registration'


urlpatterns = [
    path('', include('tom_common.urls')),
]
