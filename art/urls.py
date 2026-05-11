
from django.urls import path, include
from . import views
urlpatterns = [
    path('create_listing', views.create_listing, name='create_listing'),
]