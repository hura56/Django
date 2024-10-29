from django.db import models
from datetime import datetime
from user.models import User


class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        if self.date >= datetime.now().date():
            return f"Event: {self.title} will take place {self.date}."
        else:
            return f"Event: {self.title} took place {self.date}."


class FavouriteEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
