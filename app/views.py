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
            name, column_name, field_name = '', '', ''
            for key in params:
                if key == 'sortBy':
                    column_name = params['sortBy'][0]
                elif key in [f.name for f in RushingStatistic._meta.get_fields()]:
                    field_name = key
                    name = re.sub(r'[^A-Za-z0-9 ]+', '', params[key][0])
                    name = name.strip()

            field_name_icontains = field_name + '__icontains'
            if column_name != '' and name != '':
                stats = RushingStatistic.objects.filter(**{field_name_icontains: name}).order_by('-' + column_name)
            elif column_name != '':
                stats = RushingStatistic.objects.order_by('-' + column_name)
            elif name != '':
                stats = RushingStatistic.objects.filter(**{field_name_icontains: name})

        serializer = RushingStatisticSerializer(stats, many=True)
        return Response(serializer.data)
