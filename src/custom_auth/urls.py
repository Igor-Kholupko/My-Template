from django.urls import path, include
from . import views


urlpatterns = [
    path('signup/', views.RegistrationView.as_view(), name='signup'),
    path('', include('django.contrib.auth.urls')),
]
