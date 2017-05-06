# -*- coding: utf-8 -*-

from mediadir.AbstractSettings import AbstractSettings


class CluePluginSettings(AbstractSettings):
	def __init__(self, xbmc_addon):
		AbstractSettings.__init__(self)
		self._xbmc_addon = xbmc_addon

	def getString(self, setting_id, default_value=None):
		return self._xbmc_addon.getSetting(setting_id)

	def setString(self, setting_id, value):
		self._xbmc_addon.setSetting(setting_id, value)
