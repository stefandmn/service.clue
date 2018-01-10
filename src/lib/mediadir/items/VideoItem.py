# -*- coding: utf-8 -*-

import re
import datetime
from .BaseItem import BaseItem

__RE_IMDB__ = re.compile(r'(http(s)?://)?www.imdb.(com|de)/title/(?P<imdbid>[t0-9]+)(/)?')


class VideoItem(BaseItem):

	def __init__(self, name, uri, image=u'', fanart=u''):
		BaseItem.__init__(self, name, uri, image, fanart)
		self._genre = None
		self._aired = None
		self._duration = None
		self._director = None
		self._premiered = None
		self._episode = None
		self._season = None
		self._year = None
		self._plot = None
		self._title = name
		self._imdb_id = None
		self._cast = None
		self._rating = None
		self._track_number = None
		self._studio = None
		self._artist = None
		self._play_count = None
		self._uses_dash = None
		self._mediatype = None
		self._subtitles = None

	def setPlayCount(self, play_count):
		self._play_count = int(play_count)

	def getPlayCount(self):
		return self._play_count

	def addArtist(self, artist):
		if self._artist is None:
			self._artist = []
		self._artist.append(unicode(artist))

	def getArtist(self):
		return self._artist

	def setStudio(self, studio):
		self._studio = unicode(studio)

	def getStudio(self):
		return self._studio

	def setTitle(self, title):
		self._title = unicode(title)
		self._name = self._title

	def getTitle(self):
		return self._title

	def setTrackNumber(self, track_number):
		try:
			self._track_number = int(track_number)
		except:
			self._track_number = track_number
		pass

	def getTrackNumber(self):
		return self._track_number

	def setYear(self, year):
		self._year = int(year)

	def setYearFromDatetime(self, date_time):
		self.setYear(date_time.year)

	def getYear(self):
		return self._year

	def setPremiered(self, year, month, day):
		date = datetime.date(year, month, day)
		self._premiered = date.isoformat()

	def setPremieredFromDatetime(self, date_time):
		self.setPremiered(year=date_time.year, month=date_time.month, day=date_time.day)

	def getPremiered(self):
		return self._premiered

	def setPlot(self, plot):
		self._plot = unicode(plot)

	def getPlot(self):
		return self._plot

	def setRating(self, rating):
		self._rating = float(rating)

	def getRating(self):
		return self._rating

	def setDirector(self, director_name):
		self._director = unicode(director_name)

	def getDirector(self):
		return self._director

	def addCast(self, cast):
		if self._cast is None:
			self._cast = []
		self._cast.append(cast)

	def getCast(self):
		return self._cast

	def setImdbId(self, url_or_id):
		re_match = __RE_IMDB__.match(url_or_id)
		if re_match:
			self._imdb_id = re_match.group('imdbid')
		else:
			self._imdb_id = url_or_id
		pass

	def getImdbId(self):
		return self._imdb_id

	def setEpisode(self, episode):
		self._episode = int(episode)

	def getEpisode(self):
		return self._episode

	def setSeason(self, season):
		self._season = int(season)

	def getSeason(self):
		return self._season

	def setDuration(self, hours, minutes, seconds=0):
		_seconds = seconds
		_seconds += minutes * 60
		_seconds += hours * 60 * 60
		self.setDurationFromSeconds(_seconds)

	def setDurationFromMinutes(self, minutes):
		self.setDurationFromSeconds(int(minutes) * 60)
		pass

	def setDurationFromSeconds(self, seconds):
		self._duration = int(seconds)

	def getDuration(self):
		return self._duration

	def setAired(self, year, month, day):
		date = datetime.date(year, month, day)
		self._aired = date.isoformat()

	def setAiredFromDatetime(self, date_time):
		self.setAired(year=date_time.year, month=date_time.month, day=date_time.day)

	def getAired(self):
		return self._aired

	def setGenre(self, genre):
		self._genre = unicode(genre)
		pass

	def getGenre(self):
		return self._genre

	def setDate(self, year, month, day, hour=0, minute=0, second=0):
		date = datetime.datetime(year, month, day, hour, minute, second)
		self._date = date.isoformat(sep=' ')

	def setDateFromDatetime(self, date_time):
		self.setDate(year=date_time.year, month=date_time.month, day=date_time.day, hour=date_time.hour, minute=date_time.minute, second=date_time.second)

	def getDate(self):
		return self._date

	def setUseDash(self, value=True):
		self._uses_dash = value

	def getUseDash(self):
		return self._uses_dash is True and 'manifest/dash' in self.getUri()

	def setMediatype(self, mediatype):
		self._mediatype = mediatype

	def getMediatype(self):
		if self._mediatype not in ['video', 'movie', 'tvshow', 'season', 'episode', 'musicvideo']:
			self._mediatype = 'video'
		return self._mediatype

	def getSubtitles(self):
		return self._subtitles

	def setSubtitles(self, value):
		self._subtitles = value if value and isinstance(value, list) else None
