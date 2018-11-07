from django.urls import path

from template import views

urlpatterns = [
    path('create/', views.TemplateCreate.as_view(), name='template_create'),
    path('list/', views.TemplateList.as_view(), name='template_list'),
]
