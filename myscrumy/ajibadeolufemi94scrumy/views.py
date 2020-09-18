from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse 
from .models import User, ScrumyGoals, ScrumyHistory, GoalStatus
import random

# Create your views here.
#def get_grading_parameters(request):
#    return HttpResponse("This is a Scrum Application")

def index(request):
    goal = ScrumyGoals.objects.filter(goal_name = 'Learn Django')
    return HttpResponse( goal )
    
def move_goal (request, goal_id):
    error = {'error': "A record with that goal id does not exist"}
    try:
        goal = ScrumyGoals.objects.get(goal_id = goal_id)
    except:
        return render(request, 'ajibadeolufemi94scrumy/exception.html', error)
    return HttpResponse (goal.goal_name)

def add_goal(request):
    user = User.objects.get(username='louis')
    goal_status = GoalStatus.objects.get(status_name="Weekly Goal")
    ScrumyGoals.objects.create(goal_name="Keep Learning Django", goal_id = gen_id(), created_by="Louis", 
    moved_by = "Louis", owner="Louis", goal_status=goal_status, user=user )
    return HttpResponse('Goal has been successgully added')

def gen_id():
    id_list = ScrumyGoals.objects.all()
    id_list = [idd.goal_id for idd in id_list]
    g_id = random.randint(1000, 9999)
    if g_id in id_list:
        g_id = random.randint(1000, 9999)
    else:
        return g_id 

def home(request):
    goals = ScrumyGoals.objects.filter(goal_name='Learning Django')
    users = User.objects.all()
    weekly = GoalStatus.objects.get(status_name="Weekly Goal")
    weekly = weekly.scrumygoals_set.all()
    daily = GoalStatus.objects.get(status_name="Daily Goal")
    daily = daily.scrumygoals_set.all()
    verify = GoalStatus.objects.get(status_name="Verify Goal")
    verify = verify.scrumygoals_set.all()
    done = GoalStatus.objects.get(status_name="Done Goal")
    done = done.scrumygoals_set.all()
    goals = ScrumyGoals.objects.filter(goal_name="Learn django", goal_id= gen_id())
    
    #goals = ScrumyGoals.objects.filter(goal_name='Keep Learning Django')
    context = {
        'goals':goals,
        'users': users,
        'weekly': weekly,
        'daily':daily,
        'verify':verify,
        'done':done,
    }
    output = ', '.join([goal.goal_name for goal in goals])
    return render(request, "ajibadeolufemi94scrumy/home.html", context)

    

    
