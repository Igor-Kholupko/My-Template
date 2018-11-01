from django.urls import path
from .views import home_page

urlpatterns = [
    path('create/', home_page, name='template_create'),
]