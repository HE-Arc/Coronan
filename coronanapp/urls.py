from django.urls import path
from coronanapp import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
]