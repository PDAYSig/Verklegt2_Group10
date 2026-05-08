"""
URL configuration for Art_auctions project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='users-index'),

    path('login/', views.login, name='login'),
    path('all_art/', views.all_art, name="all_art"),

    path('profile/', views.profile, name="profile"),

    path('seller_profile/', views.seller_profile, name="seller_profile"),

    path('artwork/', views.artwork, name='artwork'),

    path('edit_profile/', views.edit_profile, name="edit_profile"),

    path('recently_sold/', views.recently_sold, name="recently_sold"),
    path('<int:id>', views.user_by_id, name='user_by_id'),

    path('login/create_user/', views.create_user, name='create_user'),

]