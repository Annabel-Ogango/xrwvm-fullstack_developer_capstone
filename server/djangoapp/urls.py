from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Path for registration
    path(route='register', view=views.registration, name='register'),

    # Path for login and logout
    path(route='login', view=views.login_user, name='login'),
    path(route='logout', view=views.logout_request, name='logout'),

    # Path for get_cars
    path(route='get_cars', view=views.get_cars, name='getcars'),

    # path for dealer reviews view (Placeholder for next steps)

    # path for add a review view (Placeholder for next steps)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)