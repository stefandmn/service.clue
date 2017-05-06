# -*- coding: utf-8 -*-

from resources.lib.mediadir.utils import DatetimeParser
from resources.lib.mediadir.items.ImageItem import ImageItem
from resources.lib.mediadir.items.AudioItem import AudioItem
from resources.lib.mediadir.items.VideoItem import VideoItem


def createFromItem(context, base_item):
	info_labels = {}
	# 'date' = '09.03.1982'
	_process_date(info_labels, base_item.getDate())
	# Image
	if isinstance(base_item, ImageItem):
		# 'title' = 'Blow Your Head Off' (string)
		_process_string_value(info_labels, 'title', base_item.getTitle())
	# Audio
	if isinstance(base_item, AudioItem):
		# 'duration' = 79 (int)
		_process_int_value(info_labels, 'duration', base_item.getDuration())
		# 'album' = 'Buckle Up' (string)
		_process_string_value(info_labels, 'album', base_item.getAlbumName())
		# 'artist' = 'Angerfist' (string)
		_process_string_value(info_labels, 'artist', base_item.getArtistName())
		# 'rating' = '0' - '5' (string)
		_process_audio_rating(info_labels, base_item.getRating())
	# Video
	if isinstance(base_item, VideoItem):
		# mediatype
		_process_mediatype(info_labels, 'mediatype', base_item.getMediatype())
		# play count
		_process_int_value(info_labels, 'playcount', base_item.getPlayCount())
		# studio
		_process_string_value(info_labels, 'studio', base_item.getStudio())
		# 'artist' = [] (list)
		_process_list_value(info_labels, 'artist', base_item.getArtist())
		# 'dateadded' = '2014-08-11 13:08:56' (string) will be taken from 'date'
		_process_video_dateadded(info_labels, base_item.getDate())
		# TODO: starting with Helix this could be seconds
		# 'duration' = '3:18' (string)
		_process_video_duration(context, info_labels, base_item.getDuration())
		# 'rating' = 4.5 (float)
		_process_video_rating(info_labels, base_item.getRating())
		# 'aired' = '2013-12-12' (string)
		_process_date_value(info_labels, 'aired', base_item.getAired())
		# 'director' = 'Steven Spielberg' (string)
		_process_string_value(info_labels, 'director', base_item.getDirector())
		# 'premiered' = '2013-12-12' (string)
		_process_date_value(info_labels, 'premiered', base_item.getPremiered())
		# 'episode' = 12 (int)
		_process_int_value(info_labels, 'episode', base_item.getEpisode())
		# 'season' = 12 (int)
		_process_int_value(info_labels, 'season', base_item.getSeason())
		# 'plot' = '...' (string)
		_process_string_value(info_labels, 'plot', base_item.getPlot())
		# 'code' = 'tt3458353' (string) - imdb id
		_process_string_value(info_labels, 'code', base_item.getImdbId())
		# 'cast' = [] (list)
		_process_list_value(info_labels, 'cast', base_item.getCast())
	# Audio and Video
	if isinstance(base_item, AudioItem) or isinstance(base_item, VideoItem):
		# 'title' = 'Blow Your Head Off' (string)
		_process_string_value(info_labels, 'title', base_item.getTitle())
		# 'tracknumber' = 12 (int)
		_process_int_value(info_labels, 'tracknumber', base_item.getTrackNumber())
		# 'year' = 1994 (int)
		_process_int_value(info_labels, 'year', base_item.getYear())
		# 'genre' = 'Hardcore' (string)
		_process_string_value(info_labels, 'genre', base_item.getGenre())
	return info_labels

def _process_date(info_labels, param):
	if param is not None and param:
		datetime = DatetimeParser.parse(param)
		datetime = '%02d.%02d.%04d' % (datetime.day, datetime.month, datetime.year)
		info_labels['date'] = datetime
	pass

def _process_int_value(info_labels, name, param):
	if param is not None:
		info_labels[name] = int(param)
	pass

def _process_string_value(info_labels, name, param):
	if param is not None:
		info_labels[name] = unicode(param)
	pass

def _process_audio_rating(info_labels, param):
	if param is not None:
		rating = int(param)
		if rating > 5:
			rating = 5
		if rating < 0:
			rating = 0
		info_labels['rating'] = unicode(rating)
	pass

def _process_video_dateadded(info_labels, param):
	if param is not None and param:
		info_labels['dateadded'] = param
	pass

def _process_video_duration(context, info_labels, param):
	if param is not None:
		info_labels['duration'] = '%d' % param
	pass

def _process_video_rating(info_labels, param):
	if param is not None:
		rating = float(param)
		if rating > 10.0:
			rating = 10.0
		if rating < 0.0:
			rating = 0.0
		info_labels['rating'] = rating
	pass

def _process_date_value(info_labels, name, param):
	if param is not None:
		date = DatetimeParser.parse(param)
		date = '%04d-%02d-%02d' % (date.year, date.month, date.day)
		info_labels[name] = date
	pass

def _process_list_value(info_labels, name, param):
	if param is not None and isinstance(param, list):
		info_labels[name] = param
	pass

def _process_mediatype(info_labels, name, param):
	info_labels[name] = param
