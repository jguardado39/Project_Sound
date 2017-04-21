# -*- coding: UTF-8 -*-

from models import Artist, Genre, Album, Song, Queue, History, Favorite
from django.contrib import admin

""" Class for Artist Admin """

class ArtistAdmin(admin.ModelAdmin):
	list_display = ('Name', )
	search_fields = ['Name']

""" Class for Genre Admin """

class GenreAdmin(admin.ModelAdmin):
	list_display = ('Name', )


""" Class for Album Admin """

class AlbumAdmin(admin.ModelAdmin):
	list_display = ('Title', )
	search_fields = ['Title']

""" Class for Song Admin """

class SongAdmin(admin.ModelAdmin):
	list_display = ('Title', 'Artist', 'Year', 'Genre', )
	search_fields = ['Title']

""" Class for Queue Admin """

class QueueAdmin(admin.ModelAdmin):
	list_display = ('Song', 'Created', )

""" Class for History Admin """

class HistoryAdmin(admin.ModelAdmin):
	list_display = ('Song', 'Created', )

""" Class for Favorite Admin """

class FavoriteAdmin(admin.ModelAdmin):
	list_display = ('Song', 'User', 'Created', )
	search_fields = ['User__username']


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Queue, QueueAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Favorite, FavoriteAdmin)