import json

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone

from dataholder.models import (
    Match,
    Score,
    Team,
)

from dataholder.api.serializers import MatchSerializer

########################################################
class TestREST(APITestCase):

    ###################################################
    def setUp(self):

        #Creating score record for testing
        score_obj = Score.objects.create(
            score1=None,
            score2=None,
            winner1=None,
            winner2=None,
        )


        #Creating team record for testing
        team1_obj = Team.objects.create(team_id=1,team_name='name1')
        team2_obj = Team.objects.create(team_id=2,team_name='bane2')

        #Creating match record for testing
        match_obj = Match.objects.create(
            id=1,
            title="Some title",
            date_start=timezone.now(),
            url='https://www.source1.org/matches/1/',
            state=1,
            bestof=3,
            tournament_id=15,
            tournament_name='Overbayes Season 1',
            score=score_obj,
            team1=team1_obj,
            team2=team2_obj
        )


    ###################################################
    def test_rest_list_view(self):
        list_url   = reverse('dataholder:api:list')
        response = self.client.get(list_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    ###################################################
    def test_rest_detail_view(self):

        detail_url = reverse('dataholder:api:detail', kwargs={'dj_id': 1})
        response = self.client.get(detail_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['title'], "Some title"
)
