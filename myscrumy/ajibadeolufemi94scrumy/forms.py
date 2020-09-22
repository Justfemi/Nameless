from django import forms
from .models import ScrumyGoals, ScrumyHistory, GoalStatus
from django.contrib.auth.models import User

class SignupForm( forms.ModelForm ):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

class CreateGoalForm( forms.ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name', 'user', 'goal_status']
        