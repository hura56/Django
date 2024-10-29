import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from event.models import Event
from event.serializers import EventSerializer
from fight.models import Fighter, WeightClass, Fight
from fight.serializers import FighterSerializer
from dateutil import parser


@api_view(['GET'])
def search(request, result):

    fighters = Fighter.objects.filter(name__icontains=result).values()
    events = Event.objects.filter(title__icontains=result).values()

    fighter_serializer = FighterSerializer(fighters, many=True)
    event_serializer = EventSerializer(events, many=True)

    return Response({
        'fighters': fighter_serializer.data,
        'events': event_serializer.data,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_upcoming_events(request):
    if not request.user.is_staff:
        return Response({'error': 'Only staff can post new events'}, status=400)

    url = 'https://mmafightcardsapi.adaptable.app'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        events = data.get('data', [])
        weight_class_object, created = WeightClass.objects.get_or_create(name='Default', weight=500)

        for event in events:
            title = event.get('title')
            date_str = event.get('date')
            date_temp = parser.parse(date_str)
            date = date_temp.strftime("%Y-%m-%d")

            event_object, created = Event.objects.get_or_create(title=title, date=date)

            fights = event.get('fights', [])
            for fight in fights:
                fighter1_name = fight.get('fighterA', {}).get('name')
                fighter1_record = fight.get('fighterA', {}).get('record')
                fighter2_name = fight.get('fighterB', {}).get('name')
                fighter2_record = fight.get('fighterB', {}).get('record')
                fighter1, created = Fighter.objects.get_or_create(name=fighter1_name, record=fighter1_record)
                fighter2, created = Fighter.objects.get_or_create(name=fighter2_name, record=fighter2_record)
                fight_object, created = Fight.objects.get_or_create(event=event_object, fighter1=fighter1, fighter2=fighter2)

        return Response({'message': 'Data from API saved successfully'})
    else:
        return Response({'error': 'Could not get data from API'}, status=response.status_code)





