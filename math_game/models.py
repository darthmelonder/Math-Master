from __future__ import unicode_literals

from django.db import models

# Create your models here.
	
class Game (models.Model):
	game_id = models.IntegerField(default=0);
	no_of_players = models.IntegerField(default=2)
	winner = models.CharField(max_length=50);
	answer = models.IntegerField(default=0);
	question = models.CharField(max_length=200);
	rounds = models.IntegerField(default=200)
	seconds = models.IntegerField(default=3600);
	rounds_over = models.IntegerField(default=0);
	seconds_over = models.IntegerField(default=0);
	start_time = models.IntegerField(default=0);
	def __str__(self):
		return str(self.game_id);

class Player (models.Model):
	name = models.CharField (max_length=200);
	game = models.ForeignKey(Game, on_delete=models.CASCADE);
	wins = models.IntegerField(default=0)
	def __str__(self):
		return self.name;from django.db import models

