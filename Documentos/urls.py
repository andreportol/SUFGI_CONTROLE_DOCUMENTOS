from django.urls import path
from .views import IndexTemplateView

app_name = 'Documentos'

urlpatterns = [
    path('',IndexTemplateView.as_view(), name='index')
]