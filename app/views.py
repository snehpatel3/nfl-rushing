from .serializers import RushingStatisticSerializer
from .models import RushingStatistic

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status

import re

# Create your views here.
class RushingStatisticsList(APIView):
    def get(self, request, format=None):
        params = dict(request.query_params)
        stats = {}
        if not params:
            stats = RushingStatistic.objects.all()
        else:
            name = ''
            if 'filterBy' in params:
                name = re.sub(r'[^A-Za-z0-9 ]+', '', params['filterBy'][0])
                name = name.strip()

            column_name = ''
            if 'sortBy' in params:
                column_name = params['sortBy'][0]

            if column_name != '' and name != '':
                stats = RushingStatistic.objects.filter(player__icontains=name).order_by('-' + column_name)
            elif column_name != '':
                stats = RushingStatistic.objects.order_by('-' + column_name)
            elif name != '':
                stats = RushingStatistic.objects.filter(player__icontains=name)

        serializer = RushingStatisticSerializer(stats, many=True)
        return Response(serializer.data)
