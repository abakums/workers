from django.urls import path
from . import views

urlpatterns = [
    path('', views.WorkersListView.as_view(), name='get_workers'),
]
