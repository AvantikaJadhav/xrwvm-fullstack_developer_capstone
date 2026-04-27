from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path(route='', view=views.get_dealerships, name='index'),
    path(route='about/', view=views.about, name='about'),
    path(route='contact/', view=views.contact, name='contact'),
    path(route='login/', view=views.login_request, name='login'),
    path(route='logout/', view=views.logout_request, name='logout'),
    path(route='register/', view=views.registration_request, name='register'),
    path(route='reviews/dealer/<int:dealer_id>/', view=views.get_dealer_reviews, name='dealer_reviews'),
    path(route='dealer/<int:dealer_id>/', view=views.dealer_details, name='dealer_details'),
    path(route='add_review/<int:dealer_id>/', view=views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)