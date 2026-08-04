"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # login pipeline connection
    # path("", views.login, name= "login"),

    #  dashbord
    path("", views.fastpage, name= "fastpage"),
    path("dashboard/", views.dashboard, name= "dashboard"),
    path("edit/", views.edit, name= "edit"),
    path("logout/", views.logout, name= "logout"),
    path("confirm_logout/", views.confirm_logout, name="confirm_logout"),
    path("choose_tem/", views.choose_tem, name="choose_tem"),
    path("create_resume/", views.create_resume, name= "create_resume")


    

]
