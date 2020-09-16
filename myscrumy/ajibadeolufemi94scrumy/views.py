from django.shortcuts import render
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
    scrumy = ScrumyGoals.objects.create(goal_name = 'Keep Learning Django', 
    goal_id= random.randint(1000, 9999), moved_by = 'Louis', created_by = 'Louis', 
    owner = 'Louis', goal_status = GoalStatus.objects.get(status_name = 'Weekly Goals'), 
    user = User.objects.get(username = 'louis')  )
    scrumy.save()
    return HttpResponse('Goal has been successgully added')

"""def gen_id():
    id_list = ScrumyGoals.objects.all()
    id_list = [idd.goal_id for idd in id_list]
    g_id = random.randint(1000, 9999)
    if g_id in id_list:
        g_id = random.randint(1000, 9999)
    else:
        return g_id """

def home(request):
    goals = ScrumyGoals.objects.filter(goal_name='Keep Learning Django')
    output = ', '.join([goal.goal_name for goal in goals])
    return HttpResponse(output)

    

    
