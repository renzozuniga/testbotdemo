from django.db import models
from django.db import connections

# Create your models here.
class UsersBot(models.Model):
	user_id = models.CharField(max_length=200)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Conversations(models.Model):
	user_id = models.CharField(max_length=200)
	message_in = models.CharField(max_length=200)
	message_out = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class FavoriteSongs(models.Model):
	user_id = models.CharField(max_length=200)
	track_name = models.CharField(max_length=200)
	artist_name = models.CharField(max_length=200)

