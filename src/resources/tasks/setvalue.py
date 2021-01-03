# -*- coding: utf-8 -*-

from abcgraphic import GraphicTask



class SetValue(GraphicTask):
	key = "setvalue"


	def _presetup(self):
		if self._window is not None:
			try:
				self._control = self._window.getControl(self._control)
			except:
				self._control = None
				self.error("No control found within identified window")
		if self._default is None and self._control is not None:
			self._default = self._control.getValue()
			self._default = '' if self._default is None else self._default
			self.debug("Getting control default value: %s" %str(self._default))


	def _setup(self):
		if self._control is not None and self._data is not None:
			self.debug('Setting control value: %s' %str(self._data))
			self._control.setValue(str(self._data))
