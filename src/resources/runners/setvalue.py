# -*- coding: utf-8 -*-

from setlabel import SetLabel



class SetValue(SetLabel):


	def code(self):
		return "setvalue"


	def _get(self, control):
		data = None
		if control is not None:
			data = control.getValue()
			data = '' if data is None else data
			self.debug("Getting control value: %s" %str(data))
		return data


	def _set(self, control, data):
		if control is not None and data is not None:
			self.debug('Setting control value: %s' %str(data))
			control.setValue(str(data))