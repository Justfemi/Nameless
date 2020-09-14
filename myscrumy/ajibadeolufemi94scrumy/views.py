from django.shortcuts import render
from django.http import HttpResponse 
from .models import ScrumyGoals, ScrumyHistory, GoalStatus


# Create your views here.
#def get_grading_parameters(request):
#    return HttpResponse("This is a Scrum Application")

def index(request):
    goal = ScrumyGoals.objects.filter(goal_name = 'Learn Django')
    return HttpResponse( goal )

def move_goal(request, goal_id):

    dictionary = {
        'error': "Goal id doesn't exist"
    }
    try:
        goal = ScrumyGoals.objects.get(goal_id = goal_id)
    except:
        return render(request, 'exception.html', dictionary)
    return HttpResponse (goal.goal_name)


    

    
