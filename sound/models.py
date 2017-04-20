#-*- coding:; UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
import time

""" Class for Artists """

class Artist(models.Model):
	class Meta: # Available permission/associated database table name/abstract or not
		ordering = ['Name']

	def __unicode__(self):
		return "%s" % self.Name #formatting string to return Name

	Name = models.CharField(max_length = 200) #

""" Class for Genre """

class Genre(models.Model):
	class Meta:
		ordering = ['Name']

	def __unicode__(self):
		return "%s" % self.Name #formatting string to return Title

	Name = models.CharField(max_length = 200)

""" Class for Albums"""

class Album(models.Model):
	class Meta:
		ordering = ['Title']

	def __unicode__(self):
		return "%s" % self.Title

	Title = models.CharField(max_length = 200)

""" Class for Songs"""
	
class Song(models.Model):
	class Meta:
		ordering = ['Title', 'Artist', 'Album']

	def __unicode__(self):
		return "%s - %s" % (self.Artist.Name, self.Title)

	Artist = models.ForeignKey(Artist)
	Album = models.ForeignKey(Album, null = True)
	Filename = models.CharField(max_length = 1000)
	Genre = models.ForeignKey(Genre, null = True)
	Length = models.IntegerField()
	Ttile = models.CharField(max_length = 200)
	Year = models.IntegerField(null = True)

""" Class for Queues"""

class Queue(models.Model):
	Creatred = models.DateTimeField(auto_now_add = True)
	Song = models.ForeignKey(Song, unique = True)
	User = models. ManyToMany Field(User)

""" Class for Favorite"""

class Favorite(models.Model):
	class Meta:
		unique_together = ("Song", "User")
		ordering = ['-Created']

	Created = models.DateTimeField(auto_now_add = True)
	Song = models.ForeignKey(Song)
	User = models.ForeignKey(User)

""" Class for History"""

class History(models.Model)
	class Meta:
		ordering = ['-Created']

	Created = models.DateTimeField(auto_now_add = True)
	Song = models.ForeignKey(Song)
	User = models.ManyToManyField(User, null = True)

""" Class for Player"""

class Player(models.Model):
	Pid = models.IntegerField()

""" Class for QueueFeed"""

class QueueFeed(Feed):
	description = "Top song in the queue"
	link = "/queue/"
	title = "Sound Queue Feed"

	def items(self):
		return Queue.objects.all()[:1]

	def item_title(self, item):
		return item.Song.Title

	def item_description(self, item):
		return unicode(item.Song.Title) + " by " + \
				unicode(item.Song.Artist) + " from " + \
				unicode(item.Song.Album)

	def item_link(self, item):
		# Will figure out how to put url on item
		return "/queue/#" + unicode(int(round(time.time() * 1000)))