from django.contrib import admin
from event.models import Event
from fight.models import Fighter, Fight, WeightClass
from .forms import EventAdminForm, FighterAdminForm, FightAdminForm, WeightClassAdminForm


class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ('title', 'date')
    search_fields = ('title', 'date')


class FighterAdmin(admin.ModelAdmin):
    form = FighterAdminForm
    list_display = ('name', 'age', 'weight_class', 'record')
    search_fields = ['name']


class FightAdmin(admin.ModelAdmin):
    form = FightAdminForm
    list_display = ('fighter1', 'fighter2', 'event')
    search_fields = ('fighter1__name', 'fighter2__name', 'event__title')


class WeightClassAdmin(admin.ModelAdmin):
    form = WeightClassAdminForm
    list_display = ('name', 'weight')
    search_fields = ('name', 'weight')


admin.site.register(Event, EventAdmin)
admin.site.register(Fighter, FighterAdmin)
admin.site.register(Fight, FightAdmin)
admin.site.register(WeightClass, WeightClassAdmin)
