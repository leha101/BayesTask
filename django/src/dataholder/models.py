from django.db import models

##########################################################
### ============= MODELS DEFINITIONS ==================###
##########################################################

######################################################
class Team(models.Model):
    team_id = models.PositiveIntegerField(default=0)
    team_name = models.CharField(max_length=150)

######################################################
class Score(models.Model):
    score1  = models.PositiveIntegerField(null=True,blank=True)
    score2  = models.PositiveIntegerField(null=True,blank=True)
    winner1 = models.BooleanField(null=True,blank=True)
    winner2 = models.BooleanField(null=True,blank=True)

######################################################
class Match(models.Model):
    dj_id           = models.AutoField(primary_key=True)
    id              = models.CharField(max_length=150,null=True,blank=True)
    title           = models.CharField(max_length=150)
    date_start      = models.DateTimeField(auto_now=False,auto_now_add=False)
    url             = models.URLField(max_length = 200)
    state           = models.PositiveIntegerField(default=0)
    bestof          = models.PositiveIntegerField(null=True,blank=True)
    tournament_id   = models.PositiveIntegerField(null=True,blank=True)
    tournament_name = models.CharField(max_length=150)
    score           = models.ForeignKey(Score,on_delete=models.CASCADE)
    team1           = models.ForeignKey(Team, related_name='team1', on_delete=models.CASCADE)
    team2           = models.ForeignKey(Team, related_name='team2', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
