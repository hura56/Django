from rest_framework import serializers
from event.serializers import EventSerializer
from .models import Fighter, Fight, WeightClass, Comment
from user.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for fight comment object"""
    user_added = UserSerializer(read_only=True)
    date_added = serializers.DateField(read_only=True, format='%d %B %Y')

    class Meta:
        model = Comment
        fields = (
            'id',
            'user_added',
            'content',
            'date_added',
            'fight',
        )
        write_only_fields = (
            'fight',
        )


class FighterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fighter
        fields = (
            'id',
            'name',
        )


class WeightClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightClass
        fields = (
            'name',
        )


class FightSerializer(serializers.ModelSerializer):
    """Serializer for fight object"""
    event = EventSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True, source='comment_set')
    betting_odds = serializers.SerializerMethodField()
    fighter1 = FighterSerializer()
    fighter2 = FighterSerializer()
    weight_class = WeightClassSerializer()

    class Meta:
        model = Fight
        fields = (
            'fighter1',
            'fighter2',
            'event',
            'weight_class',
            'comments',
            'fight_date',
            'betting_odds',
        )

    def get_betting_odds(self, obj):
        return obj.betting_odds
