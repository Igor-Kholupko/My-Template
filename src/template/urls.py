from django.urls import path

from template import views

urlpatterns = [
    path('<int:pk>', views.TemplateDetail.as_view(), name='template'),
    path('create/', views.TemplateCreate.as_view(), name='template_create'),
    path('preview/<int:pk>', views.TemplatePreview.as_view(), name='template_preview'),
    path('delete/<int:pk>', views.TemplateDelete.as_view(), name='template_delete'),
    path('list/<int:user>', views.TemplateList.as_view(), name='template_list'),
]
