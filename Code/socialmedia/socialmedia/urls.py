"""socialmedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import include, path

urlpatterns = [
    path('sample/', include('app.urls')),
    path('admin/', admin.site.urls),

    path('',include('app.Authentication.urls')),
    path('home/',include('app.Authentication.urls')),

    path('post/',include('app.Posts.urls')),

    path('clinic/',include('app.Clinics.urls')),

    path('dashboard/',include('app.Dashboard.urls')),
    
    path('profile/',include('app.Profile.urls')),

    path('myposts/',include('app.MyPosts.urls')),

    path('myappointments/',include('app.MyAppointments.urls')),

]+static(settings.MEDIA_URL,Document_riit=settings.MEDIA_ROOT)
