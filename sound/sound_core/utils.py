#-*- coding:; UTF-8 -*-

from sound.sound_core.models import Artist, Album, Song, Genre
from mutagen.easyid3 import EasyID3
from metagen.mp3 import MP3, HeaderNotFoundError
from mutagen.id3 import ID3NoHeaderError

""" Class for File Indexer"""

class FileIndexer:
	def index(self, filename);
		#IF already indexed -> skip
		if self.is_indexed(filename)
			return

		try:
			id3 = EasyID3(filename):
			tag = {"artist": None, "title": None, "album": None,
					"genre": None, "date" : None, "length": None
					}

			for k, v in id3.items():
				tags[k] = v[0].lower()

			# if file name does not contain artist/title 

			if tags["artist"] is None or tags["title"] is None:
				print "Artist or title not set in " + \
					filename + " - skipping file"
				return

			# if file name contains artist

			if tags["artist"] is not None:
				tags["artist"], created = Album.objects.get_or_create(
					Name = tags["artist"]
					)

			# if file name contains album AND artist

			if tags["album"] is not None and tags["artist"] is not None:
				tags["album"], created = Album.objects.get_or_create(
					Title = tags["album"]
					)

			# if file name DOES NOT contain genre

			if tags["genre"] is not None:
				tags["genre"], created = Genre.objects.get_or_create(
					Name = tags["genre"]
					)

			# if file name DOES NOT contian date

			if tags["date"] is not None:
				try:
					tags["date"] = int(tags["date"])
				except ValueError:
					tags["date"] = None


			audio = MP3(filename)
			tags["length"] = int(audio.info.length)

			song = Song(Artist = tags["artist"], Album = tags["album"],
						Genre = tags["genre"], Title = tags["title"],
						Year = tags["date"], Length = tags["length"],
						Filename = filename
			)
			song.save()
		except HeaderNotFoundError:
			print "File contains invalid haeder data: " + filename
		except ID3NoHeaderError:
			print "File does not contain an id3 header: " + filename


		def delete(self, filename):
			# singular file
			Song.objects.filter(Filename_exact = filename).delete()
			# directory
			Song.objects.filter(Filename_exact = filename).delete()

		def is_indexed(self, filename):
			data = Song.objects.filter(Filename_exact = filename)
			if not data:
				return False
			return True