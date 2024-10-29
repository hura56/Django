from django.db import models
from django.contrib.auth.models import User, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from event.models import Event
from user.models import User


class WeightClass(models.Model):
    name = models.CharField(max_length=100, default='Default')
    weight = models.FloatField(default=500)  # weight in pounds (lbs)

    def __str__(self):
        return f"Weight class: {self.name}, {self.weight}"


class Fighter(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField(null=True)
    weight_class = models.ForeignKey(WeightClass, on_delete=models.DO_NOTHING, default=1)
    record = models.CharField(max_length=10, default="0:0")
    rank = models.IntegerField(null=True)

    def __str__(self):
        return self.name


# Walka

class Fight(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    fighter1 = models.ForeignKey(Fighter, related_name='fighter1', on_delete=models.CASCADE)
    fighter2 = models.ForeignKey(Fighter, related_name='fighter2', on_delete=models.CASCADE)
    winner = models.ForeignKey(Fighter, related_name='winner', null=True, blank=True, on_delete=models.DO_NOTHING)
    weight_class = models.ForeignKey(WeightClass, null=False, on_delete=models.DO_NOTHING, default=1)

    def calculate_betting_odds(self):
        import random
        fighter1_prob = random.uniform(0.1, 0.9)
        fighter2_prob = 1 - fighter1_prob
        fighter1_odds = round(1/fighter1_prob, 2)
        fighter2_odds = round(1/fighter2_prob, 2)
        return fighter1_odds, fighter2_odds

    @property
    def betting_odds(self):
        fighter1_odds, fighter2_odds = self.calculate_betting_odds()
        return {'fighter1': fighter1_odds, 'fighter2': fighter2_odds}

    @property
    def fight_date(self):
        return self.event.date if self.event else None

    def __str__(self):
        return f"{self.fighter1.name} vs {self.fighter2.name}"


class Comment(models.Model):
    """fight comment model"""
    content = models.TextField()
    date_added = models.DateField(auto_now=True)
    user_added = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    fight = models.ForeignKey(Fight, null=True, on_delete=models.CASCADE)


class FavouriteFighter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fighter = models.ForeignKey(Fighter, on_delete=models.CASCADE)


class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fight = models.ForeignKey(Fight, on_delete=models.CASCADE)
    winner_prediction = models.ForeignKey(Fighter, null=True, blank=True, on_delete=models.SET_NULL)
