from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class GoalStatus( models.Model ):
    status_name = models.CharField( max_length=20 )
    def __str__( self ):
        return self.status_name

class ScrumyGoals( models.Model ):
    goal_name = models.CharField( max_length=100 )
    goal_id = models.IntegerField( default=20 )
    created_by = models.CharField( max_length=30 )
    moved_by = models.CharField( max_length=30 )
    owner = models.CharField( max_length= 30 )
    goal_status = models.ForeignKey( 
        GoalStatus, 
        on_delete = models.PROTECT, null=True )
    user = models.ForeignKey(
        User,
        related_name='user',
        on_delete = models.PROTECT )
    def __str__( self ):
       return self.goal_name

class ScrumyHistory( models.Model ):
    moved_by = models.CharField( max_length= 30 )
    created_by = models.CharField( max_length= 30 )
    moved_from = models.CharField( max_length= 30 )
    moved_to = models.CharField( max_length= 30 )
    time_of_action = models.DateTimeField( auto_now= False, auto_now_add= True)
    goal = models.ForeignKey( ScrumyGoals, on_delete = models.CASCADE )
    def __str__( self ):
        return self.created_by

