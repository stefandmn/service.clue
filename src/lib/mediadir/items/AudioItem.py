# -*- coding: utf-8 -*-

from .BaseItem import BaseItem


class AudioItem(BaseItem):

	def __init__(self, name, uri, image=u'', fanart=u''):
		BaseItem.__init__(self, name, uri, image, fanart)
		self._duration = None
		self._track_number = None
		self._year = None
		self._genre = None
		self._album = None
		self._artist = None
		self._title = name
		self._rating = None

	def setRating(self, rating):
		self._rating = float(rating)

	def getRating(self):
		return self._rating

	def setTitle(self, title):
		self._title = unicode(title)

	def getTitle(self):
		return self._title

	def setArtistName(self, artist_name):
		self._artist = unicode(artist_name)

	def getArtistName(self):
		return self._artist

	def setAlbumName(self, album_name):
		self._album = unicode(album_name)

	def getAlbumName(self):
		return self._album

	def setGenre(self, genre):
		self._genre = unicode(genre)

	def getGenre(self):
		return self._genre

	def setYear(self, year):
		self._year = int(year)

	def setYearFromDatetime(self, date_time):
		self.setYear(date_time.year)

	def getYear(self):
		return self._year

	def setTrackNumber(self, track_number):
		self._track_number = int(track_number)

	def getTrackNumber(self):
		return self._track_number

	def setDurationFromMilliSeconds(self, milli_seconds):
		self.setDurationFromSeconds(int(milli_seconds)/1000)

	def setDurationFromSeconds(self, seconds):
		self._duration = int(seconds)

	def setDurationFromMinutes(self, minutes):
		self.setDurationFromSeconds(int(minutes)*60)

	def getDuration(self):
		return self._duration
