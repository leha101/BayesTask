from django.db import models

# Create your models here.
class Team(models.Model):
    team = models.PositiveIntegerField(default=0)
    te_name = models.CharField(max_length=150)
