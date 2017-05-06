# -*- coding: utf-8 -*-

import sys
import urllib
import urlparse
import weakref
import datetime
import json
import xbmc
import xbmcvfs
import xbmcaddon
import xbmcplugin
import CommonFunctions as common
from mediadir.utils.Utilities import to_unicode
from mediadir.AbstractContext import AbstractContext
from .CluePluginSettings import CluePluginSettings
from .ClueContextUI import ClueContextUI
from .ClueSystemVersion import ClueSystemVersion
from .CluePlaylist import CluePlaylist
from .CluePlayer import CluePlayer


class ClueContext(AbstractContext):

	def __init__(self, path='/', params=None, plugin_name=u'', plugin_id=u'', override=True):
		AbstractContext.__init__(self, path, params, plugin_name, plugin_id)
		if plugin_id:
			self._addon = xbmcaddon.Addon(id=plugin_id)
		else:
			self._addon = xbmcaddon.Addon()
		self._system_version = None
		# first the path of the uri
		if override:
			self._uri = sys.argv[0]
			comps = urlparse.urlparse(self._uri)
			self._path = urllib.unquote(comps.path).decode('utf-8')

			# after that try to get the params
			if len(sys.argv) > 2:
				params = sys.argv[2][1:]
				if len(params) > 0:
					self._uri = self._uri + '?' + params
					self._params = {}
					params = dict(urlparse.parse_qsl(params))
					for _param in params:
						item = params[_param]
						self._params[_param] = item.decode('utf-8')
		self._ui = None
		self._video_playlist = None
		self._audio_playlist = None
		self._video_player = None
		self._audio_player = None
		self._plugin_handle = int(sys.argv[1]) if len(sys.argv) > 1 else None
		self._plugin_id = plugin_id or self._addon.getAddonInfo('id')
		self._plugin_name = plugin_name or self._addon.getAddonInfo('name')
		self._version = self._addon.getAddonInfo('version')
		self._native_path = xbmc.translatePath(self._addon.getAddonInfo('path'))
		self._settings = CluePluginSettings(self._addon)
		# Set the data path for this addon and create the folder
		self._data_path = xbmc.translatePath('special://profile/addon_data/%s' % self._plugin_id)
		if isinstance(self._data_path, str):
			self._data_path = self._data_path.decode('utf-8')
		if not xbmcvfs.exists(self._data_path):
			xbmcvfs.mkdir(self._data_path)
		pass

	def setFormatDateShort(self, date_obj):
		date_format = xbmc.getRegion('dateshort')
		_date_obj = date_obj
		if isinstance(_date_obj, datetime.date):
			_date_obj = datetime.datetime(_date_obj.year, _date_obj.month, _date_obj.day)
		return _date_obj.strftime(date_format)

	def setFormatTime(self, time_obj):
		time_format = xbmc.getRegion('time')
		_time_obj = time_obj
		if isinstance(_time_obj, datetime.time):
			_time_obj = datetime.time(_time_obj.hour, _time_obj.minute, _time_obj.second)
		return _time_obj.strftime(time_format)

	def getLanguage(self):
		if self.getSystemVersion().getReleaseName() == 'Frodo':
			return 'en-US'
		try:
			language = xbmc.getLanguage(0, region=True)
			return language[0].lower()
		except Exception, ex:
			self.error('Failed to get system language (%s)' %str(ex))
			return 'en-US'
		pass

	def getRegion(self):
		if self.getSystemVersion().getReleaseName() == 'Frodo':
			return 'US'
		try:
			language = xbmc.getLanguage(0, region=True)
			return language[0].upper()
		except Exception, ex:
			self.error('Failed to get system region (%s)' %str(ex))
			return 'US'
		pass

	def getSystemVersion(self):
		if not self._system_version:
			self._system_version = ClueSystemVersion(version='', releasename='', appname='')
		return self._system_version

	def getVideoPlaylist(self):
		if not self._video_playlist:
			self._video_playlist = CluePlaylist('video', weakref.proxy(self))
		return self._video_playlist

	def getAudioPlaylist(self):
		if not self._audio_playlist:
			self._audio_playlist = CluePlaylist('audio', weakref.proxy(self))
		return self._audio_playlist

	def getVideoPlayer(self):
		if not self._video_player:
			self._video_player = CluePlayer('video', weakref.proxy(self))
		return self._video_player

	def getAudioPlayer(self):
		if not self._audio_player:
			self._audio_player = CluePlayer('audio', weakref.proxy(self))
		return self._audio_player

	def getUI(self):
		if not self._ui:
			self._ui = ClueContextUI(self._addon, weakref.proxy(self))
		return self._ui

	def getHandle(self):
		return self._plugin_handle

	def getDataPath(self):
		return self._data_path

	def getNativePath(self):
		return self._native_path

	def getSettings(self):
		return self._settings

	def localize(self, text_id, default_text=u''):
		if isinstance(text_id, int):
			if text_id >= 0:
				result = xbmc.getLocalizedString(text_id)
				if result is not None and result:
					return to_unicode(result)
		result = self._addon.getLocalizedString(int(text_id))
		if result is not None and result:
			return to_unicode(result)
		return to_unicode(default_text)

	def setContentType(self, content_type):
		self.debug('Setting content-type: "%s" for "%s"' % (content_type, self.getPath()))
		xbmcplugin.setContent(self._plugin_handle, content_type)

	def addSortMethod(self, *sort_methods):
		for sort_method in sort_methods:
			xbmcplugin.addSortMethod(self._plugin_handle, sort_method)
		pass

	def clone(self, new_path=None, new_params=None):
		if not new_path:
			new_path = self.getPath()
		if not new_params:
			new_params = self.getParams()
		new_context = ClueContext(path=new_path, params=new_params, plugin_name=self._plugin_name, plugin_id=self._plugin_id, override=False)
		new_context._function_cache = self._function_cache
		new_context._search_history = self._search_history
		new_context._favorite_list = self._favorite_list
		new_context._watch_later_list = self._watch_later_list
		new_context._access_manager = self._access_manager
		new_context._ui = self._ui
		new_context._video_playlist = self._video_playlist
		new_context._video_player = self._video_player
		return new_context

	def execute(self, command):
		xbmc.executebuiltin(command)

	def sleep(self, milli_seconds):
		xbmc.sleep(milli_seconds)

	def isAddonEnabled(self, addon_id):
		rpc_request = json.dumps({"jsonrpc": "2.0", "method": "Addons.GetAddonDetails", "id": 1, "params": {"addonid": "%s" % addon_id, "properties": ["enabled"]} })
		response = json.loads(xbmc.executeJSONRPC(rpc_request))
		try:
			return response['result']['addon']['enabled'] is True
		except KeyError:
			message = response['error']['message']
			code = response['error']['code']
			common.debug('Requested |%s| received error |%s| and code: |%s|' % (rpc_request, message, code))
			return False

	def setAddonEnabled(self, addon_id, enabled=True):
		rpc_request = json.dumps({"jsonrpc": "2.0", "method": "Addons.SetAddonEnabled", "id": 1, "params": {"addonid": "%s" % addon_id, "enabled": enabled} })
		response = json.loads(xbmc.executeJSONRPC(rpc_request))
		try:
			return response['result'] == 'OK'
		except KeyError:
			message = response['error']['message']
			code = response['error']['code']
			common.debug('Requested |%s| received error |%s| and code: |%s|' % (rpc_request, message, code))
			return False
