from django import forms
from event.models import Event
from fight.models import Fighter, Fight, WeightClass


class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'


class FighterAdminForm(forms.ModelForm):
    class Meta:
        model = Fighter
        fields = '__all__'


class FightAdminForm(forms.ModelForm):
    class Meta:
        model = Fight
        fields = '__all__'


class WeightClassAdminForm(forms.ModelForm):
    class Meta:
        model = WeightClass
        fields = '__all__'
