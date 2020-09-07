from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('home', views.get_grading_parameters),
]