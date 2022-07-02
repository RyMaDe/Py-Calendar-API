from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission
from .models import Calendar_API
from .serializers import Calendar_API_Serializer


class UserWritePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.Author == request.user


class CalendarListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        '''
        List all on going calendar items
        '''
        user = self.request.user
        items = Calendar_API.objects.filter(Author=user)
        serializer = Calendar_API_Serializer(items, many=True)

        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Create a calendar entry
        '''
        data = {
            'Name': request.data.get('Name'),
            'Description': request.data.get('Description'),
            'Date': request.data.get('Date'),
            'Time': request.data.get('Time'),
            'Tag': request.data.get('Tag'),
            'Author': self.request.user.id, #request.data.get('Author'),
        }
        serializer = Calendar_API_Serializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CalendarDetailApiView(APIView, UserWritePermission):
    permission_classes = [UserWritePermission]

    def get_object(self, calendar_id):
        '''
        Helper method to get the obj
        '''
        try:
            items = Calendar_API.objects.get(id=calendar_id)
            self.check_object_permissions(self.request, items)
            return items
        except Calendar_API.DoesNotExist:
            return None

    def get(self, request, calendar_id, *args, **kwargs):
        '''
        Retrieves the calendar with given id
        '''
        calendarEntry = self.get_object(calendar_id)
        if not calendarEntry:
            return Response(
                {"res": "Calendar entry does not exist"},
                status = status.HTTP_400_BAD_REQUEST
            )

        serializer = Calendar_API_Serializer(calendarEntry)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, calendar_id, *args, **kwargs):
        '''
        Updates the calendar entry
        '''
        calendarEntry = self.get_object(calendar_id)
        if not calendarEntry:
            return Response(
                {"res": "Calendar entry does not exist"},
                status = status.HTTP_400_BAD_REQUEST
            )

        data = {
            'Name': request.data.get('Name'),
            'Description': request.data.get('Description'),
            'Date': request.data.get('Date'),
            'Time': request.data.get('Time'),
            'Tag': request.data.get('Tag')
        }
        serializer = Calendar_API_Serializer(instance=calendarEntry, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, calendar_id, *args, **kwargs):
        '''
        Deletes the calendar entry
        '''
        calendarEntry = self.get_object(calendar_id)
        if not calendarEntry:
            return Response(
                {"res": "Calendar entry does not exist"},
                status = status.HTTP_400_BAD_REQUEST
            )
        calendarEntry.delete()
        return Response(
            {"res": "Calendar entry deleted"},
            status=status.HTTP_200_OK
        )


class CalendarSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        '''
        List all calendar items between two dates
        '''
        user = self.request.user
        items = Calendar_API.objects.filter(Author=user)

        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date and end_date:
            datefiltered = items.filter(Date__range=(start_date, end_date))
        elif start_date and not end_date:
            datefiltered = items.filter(Date__gte=start_date)
        elif not start_date and end_date:
            datefiltered = items.filter(Date__lte=end_date)
        else:
            datefiltered = None

        serializer = Calendar_API_Serializer(datefiltered, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
