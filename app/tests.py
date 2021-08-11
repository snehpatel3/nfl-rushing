from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .models import RushingStatistic
from .serializers import RushingStatisticSerializer
from rest_framework import status

class RushingStatisticsListTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.api_url = reverse('statistics-list')

    def test_all_records_exist(self):
        stats = RushingStatistic.objects.all()
        response = self.client.get(self.api_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = RushingStatisticSerializer(stats, many=True)
        self.assertEquals(serializer.data, response.data)

    def test_count_all_records(self):
        stats = RushingStatistic.objects.all()
        response = self.client.get(self.api_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = RushingStatisticSerializer(stats, many=True)
        self.assertEquals(len(serializer.data), len(response.data))

    def test_sortBy_lng(self):
        stats = RushingStatistic.objects.order_by('-lng')
        response = self.client.get(self.api_url, {'sortBy': 'lng'})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = RushingStatisticSerializer(stats, many=True)
        self.assertEquals(serializer.data, response.data)
    
    def test_sortBy_td(self):
        stats = RushingStatistic.objects.order_by('-td')
        response = self.client.get(self.api_url, {'sortBy': 'td'})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = RushingStatisticSerializer(stats, many=True)
        self.assertEquals(serializer.data, response.data)

    def test_sortBy_yds(self):
        stats = RushingStatistic.objects.order_by('-yds')
        response = self.client.get(self.api_url, {'sortBy': 'yds'})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = RushingStatisticSerializer(stats, many=True)
        self.assertEquals(serializer.data, response.data)

    def test_filter_player_jay(self):
        stats = RushingStatistic.objects.filter(player__icontains='Jay')
        response = self.client.get(self.api_url, {'player': 'Jay'})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = RushingStatisticSerializer(stats, many=True)
        self.assertEquals(serializer.data, response.data)

    def test_filter_player_uppercase_lowercase_should_be_same(self):
        stats = RushingStatistic.objects.filter(player__icontains='Jay')
        response = self.client.get(self.api_url, {'player': 'jay'})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = RushingStatisticSerializer(stats, many=True)
        self.assertEquals(serializer.data, response.data)

    def test_sortby_filter_player_jay_lng(self):
        stats = RushingStatistic.objects.filter(player__icontains='Jay').order_by('-lng')
        response = self.client.get(self.api_url, {'player': 'Jay', 'sortBy': 'lng'})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = RushingStatisticSerializer(stats, many=True)
        self.assertEquals(serializer.data, response.data)

    def test_sortby_filter_player_shaun_td(self):
        stats = RushingStatistic.objects.filter(player__icontains='Shaun').order_by('-td')
        response = self.client.get(self.api_url, {'player': 'Shaun', 'sortBy': 'td'})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = RushingStatisticSerializer(stats, many=True)
        self.assertEquals(serializer.data, response.data)

    def test_sortby_filter_player_ty_yds(self):
        stats = RushingStatistic.objects.filter(player__icontains='Ty').order_by('-yds')
        response = self.client.get(self.api_url, {'player': 'Ty', 'sortBy': 'yds'})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        serializer = RushingStatisticSerializer(stats, many=True)
        self.assertEquals(serializer.data, response.data)
