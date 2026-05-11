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
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='users-index'),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('all_art/', views.all_art, name="all_art"),

    path('profile/', views.profile, name="profile"),

    path("seller/<int:id>/", views.seller_profile, name="seller_profile"),

    path('artwork/<int:id>/', views.artwork, name='artwork'),

    path('edit_profile/', views.edit_profile, name="edit_profile"),

    path('recently_sold/', views.recently_sold, name="recently_sold"),
    path('<int:id>', views.user_by_id, name='user_by_id'),

    path('login/register/', views.register, name='register'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)