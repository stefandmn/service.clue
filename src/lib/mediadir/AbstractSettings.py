# -*- coding: utf-8 -*-

import CommonFunctions as common


class AbstractSettings(object):
	def __init__(self):
		object.__init__(self)
		pass

	def getString(self, setting_id, default_value=None):
		raise NotImplementedError()

	def setString(self, setting_id, value):
		raise NotImplementedError()

	def openSettings(self):
		raise NotImplementedError()

	def getInt(self, setting_id, default_value, converter=None):
		if not converter:
			converter = lambda x: x
			pass
		value = self.getString(setting_id)
		if value is None or value == '':
			return default_value
		try:
			return converter(int(value))
		except Exception, ex:
			common.error("Failed to get setting '%s' as 'int' (%s)" % setting_id, ex.__str__())
			pass
		return default_value

	def setInt(self, setting_id, value):
		self.setString(setting_id, str(value))
		pass

	def setBool(self, setting_id, value):
		if value:
			self.setString(setting_id, 'true')
		else:
			self.setString(setting_id, 'false')

	def getBool(self, setting_id, default_value):
		value = self.getString(setting_id)
		if value is None or value == '':
			return default_value
		if value != 'false' and value != 'true':
			return default_value
		return value == 'true'

	def getItemsPerPage(self):
		return self.getInt('content.max_per_page', 50, lambda x: (x + 1) * 5)

	def getVideoQuality(self, quality_map_override=None):
		vq_dict = {0:240, 1:360, 2:480, 3:720, 4:1080, 5:2160, 6:4320}
		if quality_map_override is not None:
			vq_dict = quality_map_override
			pass
		vq = self.getInt('video.quality', 1)
		return vq_dict[vq]

	def ask4VideoQuality(self):
		return self.getBool('video.quality', False)

	def showFanart(self):
		return self.getBool('fanart.show', True)

	def getSearchHistorySize(self):
		return self.getInt('search.size', 5, lambda x: x * 5)

	def isSupportAlternativePlayerEnabled(self):
		return self.getBool('support.alternative_player', False)

	def getUseDash(self):
		return self.getBool('video.quality.mpd', False)

	def getDashSupportBuiltin(self):
		return self.getBool('video.support.mpd.builtin', False)

	def getDashSupportAddon(self):
		return self.getBool('video.support.mpd.addon', False)

	def getSubtitleLanguages(self):
		return self.getInt('subtitle.languages', 0)

	def getRequiresDualLogin(self):
		return self.getBool('youtube.folder.my_subscriptions.show', True)
