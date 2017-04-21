# -*- coding: UTF-8 -*-

from django.core.paginator import Paginator, InvalidPage
from django.core.expections import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Count, Min, Q
from django.contrib.sessions.models import Session
from django.utils import formats
import os, re, time
from datetime import datetime
from signal import SIGABRT
from django.contrib.auth.models import User
from models import Song, Artist, Album, Genre, Queue, Favorite, History, Player


class api_base:
	count = 30
	user_id = None
	search_term = None
	search_artist_name = None
	search_album_title = None
	filter_year = None
	filter_genre = None
	filter_album_id = None
	filter_artist_id = None
	order_by_field = None
	order_by_direction = None
	order_by_fields = []
	order_by_direction = ["asc", "desc"]
	orde_by_default = None

	def set_count(self, count):
		if count > 100:
			self.count = 100
		elif count > 0:
			self.count = count

	def set_user_id(self, user_id):
		self.user_id = user_id