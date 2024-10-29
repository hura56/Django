import django_filters
from event.models import Event
from .models import Fight


class FightFilter(django_filters.rest_framework.FilterSet):
    """Filters for fight list"""
    event = django_filters.ModelMultipleChoiceFilter(to_field_name='id', queryset=Event.objects.all())

    class Meta:
        model = Fight
        fields = ('event', 'fighter1', 'fighter2', 'winner', 'weight_class')
