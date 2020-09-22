from django.urls import path, include
from . import views

urlpatterns = [
#   path('', views.get_grading_parameters),
    path('', views.index, name='index'),
    path('movegoal/<int:goal_id>', views.move_goal, name='move goal'),
    path('addgoal', views.add_goal, name='add goal'),
    path('home', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('welcome', views.success, name='success'),
]