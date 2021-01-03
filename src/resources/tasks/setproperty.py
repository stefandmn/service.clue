# -*- coding: utf-8 -*-

from abcgraphic import GraphicTask
import common


class SetProperty(GraphicTask):
	key = "setproperty"


	def _presetup(self):
		if self._default is None and self._property is not None:
			self._default = common.getSkinProperty(self._wid, self._property)


	def _setup(self):
		if self._data is not None and self._property is not None:
			self.trace('Setting [%s] window property with value: %s' %(self._property, str(self._data)))
			#self._window.setProperty(self._property, str(self._data ))
			# nasty workaround for Kodi bug
			common.runBuiltinCommand("SetProperty", param=self._property, values=str(self._data), wait=True)
		elif self._data == '' and self._property is not None:
			self.debug('Making [%s] window property empty' %self._property)
			#self._window.setProperty(self._property, "")
			# nasty workaround for Kodi bug
			common.runBuiltinCommand("SetProperty", param=self._property, values="", wait=True)
