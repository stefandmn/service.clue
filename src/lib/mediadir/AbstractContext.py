# -*- coding: utf-8 -*-

import os
import urllib
import CommonFunctions as common
from mediadir.utils.Utilities import *
from mediadir.utils.FunctionCache import FunctionCache
from mediadir.utils.SearchHistory import SearchHistory
from mediadir.utils.FavoriteList import FavoriteList
from mediadir.utils.WatchLaterList import WatchLaterList
from mediadir.utils.AccessManager import AccessManager


class AbstractContext(object):

	def __init__(self, path=u'/', params=None, plugin_name=u'', plugin_id=u''):
		if not params:
			params = {}
		self._cache_path = None
		self._function_cache = None
		self._search_history = None
		self._favorite_list = None
		self._watch_later_list = None
		self._access_manager = None
		self._plugin_name = unicode(plugin_name)
		self._version = 'UNKNOWN'
		self._plugin_id = plugin_id
		self._path = createPath(path)
		self._params = params
		self._utils = None
		self._view_mode = None
		# create valid uri
		self._uri = self.createUri(self._path, self._params)

	def setFormatDateShort(self, date_obj):
		raise NotImplementedError()

	def setFormatTime(self, time_obj):
		raise NotImplementedError()

	def getLanguage(self):
		raise NotImplementedError()

	def getRegion(self):
		raise NotImplementedError()

	def _getCachePath(self):
		if not self._cache_path:
			self._cache_path = os.path.join(self.getDataPath(), 'cache')
		return self._cache_path

	def getFunctionCache(self):
		if not self._function_cache:
			max_cache_size_mb = self.getSettings().getInt('cache.size', 5)
			self._function_cache = FunctionCache(os.path.join(self._getCachePath(), 'cache'), max_file_size_kb=max_cache_size_mb * 1024)
		return self._function_cache

	def getSearchHistory(self):
		if not self._search_history:
			max_search_history_items = self.getSettings().getInt('search.size', 5, lambda x: x * 5)
			self._search_history = SearchHistory(os.path.join(self._getCachePath(), 'search'), max_search_history_items)
		return self._search_history

	def getFavoriteList(self):
		if not self._favorite_list:
			self._favorite_list = FavoriteList(os.path.join(self._getCachePath(), 'favorites'))
		return self._favorite_list

	def getWatchLaterList(self):
		if not self._watch_later_list:
			self._watch_later_list = WatchLaterList(os.path.join(self._getCachePath(), 'watch_later'))
		return self._watch_later_list

	def getAccessManager(self):
		if not self._access_manager:
			self._access_manager = AccessManager(self.getSettings())
		return self._access_manager

	def getVideoPlaylist(self):
		raise NotImplementedError()

	def getAudioPlaylist(self):
		raise NotImplementedError()

	def getVideoPlayer(self):
		raise NotImplementedError()

	def getAudioPlayer(self):
		raise NotImplementedError()

	def getUI(self):
		raise NotImplementedError()

	def getSystemVersion(self):
		raise NotImplementedError()

	def createUri(self, path=u'/', params=None):
		if not params:
			params = {}
		uri = createUriPath(path)
		if uri:
			uri = "%s://%s%s" % ('plugin', self._plugin_id.encode('utf-8'), uri)
		else:
			uri = "%s://%s/" % ('plugin', self._plugin_id.encode('utf-8'))
		if len(params) > 0:
			# make a copy of the map
			uri_params = {}
			uri_params.update(params)
			# encode in utf-8
			for param in uri_params:
				if isinstance(params[param], int):
					params[param] = str(params[param])
				uri_params[param] = to_utf8(params[param])
			uri += '?' + urllib.urlencode(uri_params)
		return uri

	def getPath(self):
		return self._path

	def getParams(self):
		return self._params

	def getParam(self, name, default=None):
		return self.getParams().get(name, default)

	# Returns the path for read/write access of files
	def getDataPath(self):
		raise NotImplementedError()

	def getNativePath(self):
		raise NotImplementedError()

	def getIcon(self):
		return os.path.join(self.getNativePath(), 'icon.png')

	def getFanart(self):
		return os.path.join(self.getNativePath(), 'fanart.jpg')

	def createResourcePath(self, *args):
		path_comps = []
		for arg in args:
			path_comps.extend(arg.split('/'))
		path = os.path.join(self.getNativePath(), 'resources', *path_comps)
		return path

	def getUri(self):
		return self._uri

	def getName(self):
		return self._plugin_name

	def getVersion(self):
		return self._version

	def getId(self):
		return self._plugin_id

	def getHandle(self):
		raise NotImplementedError()

	def getSettings(self):
		raise NotImplementedError()

	def localize(self, text_id, default_text=u''):
		raise NotImplementedError()

	def setContentType(self, content_type):
		raise NotImplementedError()

	def addSortMethod(self, *sort_methods):
		raise NotImplementedError()

	def warn(self, text):
		common.warn(text)

	def error(self, text):
		common.error(text)

	def notice(self, text):
		common.notice(text)

	def debug(self, text):
		common.debug(text)

	def info(self, text):
		common.info(text)

	def clone(self, new_path=None, new_params=None):
		raise NotImplementedError()

	def execute(self, command):
		raise NotImplementedError()

	def sleep(self, milli_seconds):
		raise NotImplementedError()
