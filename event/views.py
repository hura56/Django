from .models import Event, FavouriteEvent
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import EventSerializer
from django.shortcuts import get_object_or_404


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favourite_event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return Response({'error': 'Event with given id does not exist'}, status=404)

    favourite_event, created = FavouriteEvent.objects.get_or_create(user=request.user, event=event)

    if created:
        return Response({'message': 'Event successfully added to favourites'})
    else:
        return Response({'message': 'Event is already in favourites'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favourite_events(request):
    favourite_events = FavouriteEvent.objects.filter(user=request.user)
    event_ids = favourite_events.values_list('event_id', flat=True)
    favourite_events_data = Event.objects.filter(id__in=event_ids)
    serializer = EventSerializer(favourite_events_data, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favourite_event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return Response({'error': 'Event with given id does not exist'}, status=404)

    favourite_event = get_object_or_404(FavouriteEvent, user=request.user, event=event)
    favourite_event.delete()

    return Response({'message': 'Event removed from favourites'})
