
from django.urls import path
from . import views
urlpatterns = [
    path('create_listing', views.create_listing, name='create_listing'),
]