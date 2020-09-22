from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.http import HttpResponse 
from .models import User, ScrumyGoals, ScrumyHistory, GoalStatus
import random
from .forms import SignupForm, CreateGoalForm, MoveGoalForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
#def get_grading_parameters(request):
#    return HttpResponse("This is a Scrum Application")

def index(request):
    goal = ScrumyGoals.objects.filter( goal_name = 'Learn Django' )
    #return HttpResponse( goal )
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm( request.POST )
        if form.is_valid():
            form.save( commit=False)
            cd = form.cleaned_data
            newUser = User.objects.create_user(username=cd['username'], password=form.cleaned_data['password'], email=cd['email'])
            newUser.save()
            newUser.is_staff = True
            newUser.is_superuser = True
            my_group = Group.objects.get( name='Developer' )
            my_group.user_set.add(newUser)
            return redirect ( 'success')
    else:
        form = SignupForm()
    arg = {'form':form}
    return render( request, 'ajibadeolufemi94scrumy/index.html', arg )
    
def move_goal (request, goal_id):
    context = {'goal_id': goal_id}
    move_form = MoveGoalForm()
    current_user = request.user
    group = None
    if current_user.username == 'louis':
        group
    else:
        group = current_user.groups.all()[0]
    try:

        current_user = request.user

        users_in_dev =  Group.objects.get( name='Develop' ).user_set.all()
        users_in_QA =  Group.objects.get( name='Quality Assurance' ).user_set.all()
        users_in_adm =  Group.objects.get( name='Admin' ).user_set.all()
        users_in_own =  Group.objects.get( name='Owner' ).user_set.all()
        instance = ScrumyGoals.objects.get( goal_id = goal_id )

        if request.method == 'POST':
            move_form = MoveGoalForm(request.POST, instance=instance)
            if move_form.is_valid():
                mover = move_form.save( commit=False )
                cd = move_form.cleaned_data
                goal_status = cd['goal_status'].status_name
                user = mover.user

                if current_user in users_in_dev and goal_status == 'Done Goal':
                    messages.error( request, 'Access restricted. As a Dev, you cannot move goals to done goals')
                    return HttpResponseRedirect( request.path )

                elif current_user in users_in_dev and current_user != user:
                    messages.error( request, "Access restricted. As a Dev, you cannot move other users' goals")
                    return HttpResponseRedirect( request.path )

                elif current_user in users_in_QA and goal_status == 'Weekly Goal':
                    messages.error( request, 'Access restricted. As a QA, you cannot move  goals to weeekly goals')
                    return HttpResponseRedirect( request.path )

                elif current_user in users_in_QA and current_user != user and mover.goal_status.status_name != 'Verify Goal' and goal_status != 'Done Goal':
                    messages.error( request, 'Access restricted. As a QA, you cannot move goals to weekly goals')
                    return HttpResponseRedirect( request.path )

                elif current_user in users_in_own and current_user != user:
                    messages.error( request, 'Access restricted. As a QA, you cannot move goals to done goals')
                    return HttpResponseRedirect( request.path )

                else:
                    post = mover.save()
                    return redirect( 'home' )
                    
            else:
                move_form = MoveGoalForm(instance=instance)

    except ObjectDoesNotExist:
        return render( request, 'ajibadeolufemi94scrumy/exception.html', context )

    return render( request, 'ajibadeolufemi94scrumy/move_goal.html', {'current_user': current_user,
        'users_in_dev':users_in_dev,
        'users_in_QA':users_in_QA,
        'users_in_adm':users_in_adm,
        'users_in_own':users_in_own,
        'move_form':move_form,
        } )

    #error = {'error': "A record with that goal id does not exist"}
    #try:
        #goal = ScrumyGoals.objects.get(goal_id = goal_id)
    #except:
        #return render( request, 'ajibadeolufemi94scrumy/exception.html', error )
    #return HttpResponse ( goal.goal_name )

def add_goal(request):
    current_user = request.user
    group = None
    if current_user.username == 'louis':
        group
    else:
        group = current_user.groups.all()[0]
    if request.method == "POST":
        goal_form = CreateGoalForm( request.POST )
        if goal_form.is_valid():
            cd = goal_form.cleaned_data
            add_gol = goal_form.save( commit=False )
            add_gol.goal_id = gen_id()
            add_gol.created_by = cd['user']
            add_gol.owner = cd['user']
            add_gol.moved_by = cd['user']
            goal_status = cd['goal_status'].status_name
            users_in_dev = Group.objects.get( name='Developer' ).user_set.all()
            users_in_QA = Group.objects.get( name='Quality Assurance' ).user_set.all()
            users_in_adm = Group.objects.get( name='Admin' ).user_set.all()
            users_in_own = Group.objects.get( name='Owner' ).user_set.all()

            if current_user in users_in_dev and current_user != cd['user']:
                messages.error( request, 'Access restricted, as a Dev, you can only create weekly goal for yourself ')
                return HttpResponseRedirect( request.path )
                
            if current_user in users_in_dev and goal_status != 'Weekly Goal':
                messages.error( request, 'Access restricted, as a Dev, you can only create weekly goal for yourself ')
                return HttpResponseRedirect( request.path )

            if current_user in users_in_QA and current_user != cd['user']:
                messages.error(request, 'Access restricted, as a QA, you can only create weekly goal for yourself')
                return HttpResponseRedirect( request.path )

            if current_user in users_in_adm and current_user != cd['user']:
                messages.error(request, 'Access restricted, as an admin, you can only create weekly goal for yourself')
                return HttpResponseRedirect( request.path )

            if current_user in users_in_own and current_user != cd['user']:
                messages.error( request, 'Access restricted, as an owner, you can only create weekly goal for yourself') 
                return HttpResponseRedirect( request.path )
            
            else:
                add_gol.save()
                return redirect( 'home' )
    else:
        goal_form = CreateGoalForm()
        args = {'goal_form':goal_form}
    return render( request, 'ajibadeolufemi94scrumy/add_goal.html', args )


    #user = User.objects.get(username='louis')
    #goal_status = GoalStatus.objects.get(status_name="Weekly Goal")
    #ScrumyGoals.objects.create(goal_name="Keep Learning Django", goal_id = gen_id(), created_by="Louis", 
    #moved_by = "Louis", owner="Louis", goal_status=goal_status, user=user )
    #return HttpResponse('Goal has been successgully added') 


def home(request):
    goals = ScrumyGoals.objects.filter(goal_name='Keep Learning Django')
    users = User.objects.all()
    weekly = GoalStatus.objects.get(status_name="Weekly Goal")
    weekly = weekly.scrumygoals_set.all()
    daily = GoalStatus.objects.get(status_name="Daily Goal")
    daily = daily.scrumygoals_set.all()
    verify = GoalStatus.objects.get(status_name="Verify Goal")
    verify = verify.scrumygoals_set.all()
    done = GoalStatus.objects.get(status_name="Done Goal")
    done = done.scrumygoals_set.all()
    current_user = request.user
    group = None

    if current_user.username == 'louis':
        group = group

    #goals = ScrumyGoals.objects.filter(goal_name="Learn django", goal_id= gen_id())
    #goals = ScrumyGoals.objects.filter(goal_name='Keep Learning Django')
    else: 
        group = current_user.groups.all()[0]
    context = {
        'goals':goals,
        'users':users,
        'weekly':weekly,
        'daily':daily,
        'verify':verify,
        'done':done,
        'current_user':current_user,
        'group':group,
    }
    #output = ', '.join([goal.goal_name for goal in goals])
    return render(request, "ajibadeolufemi94scrumy/home.html", context)

def gen_id():
    id_list = ScrumyGoals.objects.all()
    id_list = [idd.goal_id for idd in id_list]
    g_id = random.randint(1000, 9999)
    if g_id in id_list:
        g_id = random.randint(1000, 9999)
    else:
        return g_id 

def success(request):
    return render(request, 'ajibadeolufemi94scrumy/success.html')