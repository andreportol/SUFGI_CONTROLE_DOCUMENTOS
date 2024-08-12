from django.urls import path
from .views import IndexTemplateView

app_name = 'dashboard_documentos'

urlpatterns = [
    path('',IndexTemplateView.as_view(), name='index')
]