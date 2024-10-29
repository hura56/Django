from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import *
from datetime import datetime
from .serializers import *
from .filters import *


@api_view(['GET'])
def ranking_view(request):
    weight_classes = WeightClass.objects.all()
    rankings = {}

    for weight_class in weight_classes:
        fighters = Fighter.objects.filter(weight_class=weight_class).order_by('rank')
        rankings[weight_class.name] = [
            {
                'rank': fighter.rank,
                'name': fighter.name,
                'weight_class': fighter.weight_class.name,
                'record': fighter.record,
                'age': fighter.age,
            }
            for fighter in fighters if fighter.rank is not None
        ]
    return Response({'rankings': rankings})


class FightListView(ListAPIView):
    queryset = Fight.objects.all()
    serializer_class = FightSerializer
    filterset_class = FightFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filterset_class(self.request.GET, queryset=queryset).qs


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, fight_id, content):
    fight = get_object_or_404(Fight, pk=fight_id)
    user_added = request.user
    data = {
        'fight': fight.id,
        'user_added': user_added,
        'content': content,
    }

    comment_serializer = CommentSerializer(data=data)

    if comment_serializer.is_valid():
        comment_serializer.validated_data['user_added'] = user_added
        comment_serializer.save()
        return Response(comment_serializer.data, status=201)
    else:
        return Response(comment_serializer.errors, status=400)


@api_view(['GET'])
def get_comments(request, fight_id):
    fight = get_object_or_404(Fight, pk=fight_id)

    comments = Comment.objects.filter(fight=fight)
    comment_serializer = CommentSerializer(comments, many=True)

    return Response(comment_serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if not request.user.is_staff and comment.user_added != request.user:
        return Response({'error': 'You do not have permission to delete this comment'}, status=403)

    comment.delete()

    return Response({'message': 'Comment deleted successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favourite_fighter(request, fighter_id):
    try:
        fighter = Fighter.objects.get(pk=fighter_id)
    except Fighter.DoesNotExist:
        return Response({'error': 'Fighter with given id does not exist'}, status=404)

    favourite_fighter, created = FavouriteFighter.objects.get_or_create(user=request.user, fighter=fighter)

    if created:
        return Response({'message': 'Fighter added to favourites'})
    else:
        return Response({'message': 'Fighter is already in favourites'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favourite_fighters(request):
    favourite_fighters = FavouriteFighter.objects.filter(user=request.user)
    fighter_ids = favourite_fighters.values_list('fighter_id', flat=True)
    favourite_fighters_data = Fighter.objects.filter(id__in=fighter_ids)
    serializer = FighterSerializer(favourite_fighters_data, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favourite_fighter(request, fighter_id):
    try:
        fighter = Fighter.objects.get(pk=fighter_id)
    except Fighter.DoesNotExist:
        return Response({'error': 'Fighter with given id does not exist'}, status=404)

    favourite_fighter = get_object_or_404(FavouriteFighter, user=request.user, fighter=fighter)
    favourite_fighter.delete()

    return Response({'message': 'Fighter removed from favourites'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_prediction(request, fight_id, winner_prediction_id):
    try:
        fight = Fight.objects.get(pk=fight_id)
    except Fight.DoesNotExist:
        return Response({'error': 'fight with given id does not exist'}, status=404)

    try:
        winner_prediction = Fighter.objects.get(pk=winner_prediction_id)
    except Fighter.DoesNotExist:
        return Response({'error': 'Fighter with given id does not fight in this fight'}, status=404)

    if winner_prediction not in [fight.fighter1, fight.fighter2]:
        return Response({'error': 'Fighter with given id does not participate in this fight'})

    current_date = datetime.now().date()
    if fight.event.date < current_date:
        return Response({'error': 'The fight has already taken place'}, status=400)

    prediction, created = Prediction.objects.get_or_create(user=request.user, fight=fight)

    prediction.winner_prediction = winner_prediction
    prediction.save()

    return Response({'message': 'Prediction saved'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prediction_percentage(request, fight_id):
    try:
        fight = Fight.objects.get(pk=fight_id)
    except Fight.DoesNotExist:
        return Response({'error': 'fight with given id does not exist'}, status=404)

    total_predictions = Prediction.objects.filter(fight=fight).count()
    if total_predictions == 0:
        return Response({'error': 'No predictions for this fight'}, status=400)

    fighter1_predictions = Prediction.objects.filter(fight=fight, winner_prediction=fight.fighter1).count()
    fighter2_predictions = Prediction.objects.filter(fight=fight, winner_prediction=fight.fighter2).count()

    percentage_fighter1 = (fighter1_predictions / total_predictions) * 100
    percentage_fighter2 = (fighter2_predictions / total_predictions) * 100

    return Response({
        'fighter1': f'{percentage_fighter1:.2f}%',
        'fighter2': f'{percentage_fighter2:.2f}%'
    })

