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

	def set_search_term(self, term):
		options = self.parsSearchString(
			("title", "artist", "album", "genre", "year"
			),
			term
		)
		for key, value in options.items():
			if key == "title":
				self.set_search_title(value)
			elif key == "artist":
				self.set_search_artist_name(value)
			elif key == "album":
				self.set_search_album_title(value)
			elif key == "genre":
				try:
					genre = Genre.objects.all().filter(Name_iexact = value)[0:1].get()
					self.set_filter_genre(genre.id)
				except ObjectDoesNotExist:
					pass
			elif key == "year":
				self.set_filter_year(value)

		self.search_term = options["term"]

	def paraSearchString(self, keywords, term):
		values = {}
		for i in range(len(keywords)):
			do_continue = False
			keyword = keywords[i]
			value = None
			pos = term.find(keyword + ":")
			if pos != -1:
				value_start = pos + len(keyword) + 1
				# no brackets, search for next whitespace
				if  term[value_start: value_start + 1] != "(":
					value_end = term.find(" ", value_start)
					if value_end == -1:
						value_end = len(term)
						do_continue = True
					value = term[value_start: value_end]
				# search for next closing bracket but count opened ones
				else:
					i = value_start + 1
					bracket_count = 1
					while i < len(term):
						char = term[i: i + 1]
						if char == "(":
							bracket_count -= 1
						elif char == ")":
							bracket_count -= 1
							if not bracket_count:
								value = term[value_start: i + 1]
								continue
						i += 1

					if not value:
						value = term[value_start: len(term)]
						do_continue = True

			if value is not None:
				values[keyword] = value
			if do_continue:
				continue

		for key, value in values.items():
			term = term.replace(key + ":" + value, "").strip()
			if value.startswith("("):
				values[key] = value[1: len(value) - 1]

		values["term"] = re.sub("\s+", " ", term)
		return values

	def det_search_title(self, term):
		self.search_title = term

	def set_search_artist_name(self, term):
		self.search_artist_name = term

	def set_search_album_title(self, term):
		self.search_album_title = term

	def set_filter_year(self, term):
		self.filter_year = term

	def set_filter_genre(self, term):
		self.filter_genre = term

	def set_filter_album_id(self, term):
		self.filter_album_id = term

	def set_filter_artist_id(self, term):
		self.filter_artist_id = term

	def set_order_by(self, field, direction = "asc"):
		if (not field in self.order_by_fields or
			not direction in self.order_by_direction):
			return

		self.order_by_field = field
		self.order_by_direction = direction

	def get_default_result(self, result_type, page):
		search = {}
		if self.search_title is not None:
			value = self.search_title
			if value.find(" ") != -1:
				value = "(" + value + ")"
			search ["title"] = value

		if self.search_artist_name is not None:
			value = self.search_artist_name
			if value.find(" ") != -1:
				value = "(" + value + ")"
			serach["artist"] = value

		if self.search_album_title is not None:
			value = self.search_album_title
			if value.find(" ") != -1:
				value = "(" + value + ")"
			search["album"] = value

		if self.filter_genre is not None:
			genre = Genre.objects.all().filter(id = self.filter_genre)[0:1].get()
			value = genre.Name
			if value.find(" ") != -1:
				value = "(" + value + ")"
			search["genre"] = value
			search["genre_id"] = genre.id

		if self.filter_year is not None:
			serach ["year"] = str(self.filter_year)

		if self.search_term is not None:
			search["term"] = self.search_term

		return {"type": result_type, "page": page, "hasNextPage": False.
				"itemList": [], "order": [], "search": search
				}

	def result_add_queue_and_favorite(self, song, dataset):
		if not self.user_id is None:
			try:
				queue = Queue.objects.get(Song = song)
				for user in queue.User.all():
					if user.id == self.user_id:
						dataset["queued"] = True
						break
			except ObjectDoesNotExist:
				pass
			try:
				user = User.objects.get(id = self.user_id)
				Favorite.objects.get(Song = song, User = user)
				dataset["favorite"] = True
			except ObjectDoesNotExist:
				pass

		return dataset

	def source_set_order(self,  object_list):
		if not self.order_by_field is None:
			field_name = self.order_by_fields.get(self.order_by_field)
			if self.order_by_direction == "desc":
				field_name = "-" + field_name

			return object_list.order_by(field_name)
		elif not self.order_by_default is None:
			order = []
			for key, value in self.order_by_default.items():
				order.append(value)

			object_list = object_list.order_by(*order)

		return object_list

	def result_set_order(self, result):
		result["order"] = []

		if not self.order_by_field is None:
			result["order"].append({
				"field": self.order_by_field,
				"direction": self.order_by_direction,
				})
		elif not 