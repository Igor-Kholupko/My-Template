from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.TemplateCreate.as_view(), name='template_create'),
]
