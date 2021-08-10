from .serializers import RushingStatisticSerializer
from .models import RushingStatistic

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status

import re

# RushingStatisticsList view responsible for dealing with any listing/displaying of stats operations
class RushingStatisticsList(APIView):

    # Any GET request will be handled here 
    def get(self, request, format=None):
        # Get query params if any
        params = dict(request.query_params)
        stats = {}

        if not params:
            # Return all data if params are empty
            stats = RushingStatistic.objects.all()
        else:
            # Run thru each query param (there should be only 2 for now)
            name, column_name, field_name = '', '', ''
            for key in params:
                # Pick out the 'sortBy' value to sort specified column
                if key == 'sortBy':
                    column_name = params['sortBy'][0]
                # Pick out column name to filter by 
                elif key in [f.name for f in RushingStatistic._meta.get_fields()]:
                    field_name = key
                    name = re.sub(r'[^A-Za-z0-9 ]+', '', params[key][0])
                    name = name.strip()
            
            # Variable to store column to filter by dynamically 
            field_name_icontains = field_name + '__icontains'

            # BOTH filtering and sorting are required
            if column_name != '' and name != '':
                stats = RushingStatistic.objects.filter(**{field_name_icontains: name}).order_by('-' + column_name)
            # ONLY sorting is required
            elif column_name != '':
                stats = RushingStatistic.objects.order_by('-' + column_name)
            # ONLY filtering is required
            elif name != '':
                stats = RushingStatistic.objects.filter(**{field_name_icontains: name})

        serializer = RushingStatisticSerializer(stats, many=True)
        return Response(serializer.data)
