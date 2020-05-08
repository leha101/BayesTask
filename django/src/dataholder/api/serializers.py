from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from dataholder.models import (
    Match,
    Score,
    Team,
)

class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class ScoreSerializer(ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'

class MatchSerializer(ModelSerializer):
    score = ScoreSerializer(read_only=True)
    team1 = TeamSerializer(read_only=True)
    team2 = TeamSerializer(read_only=True)

    class Meta:
        model = Match
        fields = '__all__'

