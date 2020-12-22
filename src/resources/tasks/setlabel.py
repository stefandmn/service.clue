# -*- coding: utf-8 -*-

import sys
import common
from .abcservice import ServiceTask

if hasattr(sys.modules["__main__"], "xbmcgui"):
	xbmcgui = sys.modules["__main__"].xbmcgui
else:
	import xbmcgui


class SetLabel(ServiceTask):
	key= "setlabel"


	def code(self):
		return self.key


	def run(self, *args):
		params = dict(arg.split("=") for arg in sys.argv[2].split("&"))
		self.debug('Found parameters: %s' %str(params))
		dialog = params.get("dialog")
		dialog = 'string' if dialog is None or dialog == '' or (dialog.lower() != 'string' and dialog.lower() != 'number' and dialog.lower() != 'date' and dialog.lower() != 'time' and dialog.lower() != 'ipaddr') else dialog
		self.debug('Using dialog type: %s' % str(dialog))
		window = params.get("window")
		try:
			window = xbmcgui.getCurrentWindowId() if window is None else window
			window = xbmcgui.getCurrentWindowDialogId() if window is None else window
			if window is None:
				window = xbmcgui.Window(window)
		except BaseException as be:
			self.error("Error discovering window handler: %s" %str(be))
			window = None
		if window is not None:
			try:
				field = params.get("field")
				self.debug('Using field id: %s' % str(field))
				control = window.getControl(field)
			except:
				control = None
				self.error("No field control found within identified window")
			data = self._get(control)
			if control is not None:
				if dialog == 'string':
					data = common.StringInputDialog(default=data)
				elif dialog == 'number':
					data = common.NumberInputDialog(default=data)
				elif dialog == 'date':
					data = common.DateInputDialog(default=data)
				elif dialog == 'time':
					data = common.TimeInputDialog(default=data)
				elif dialog == 'ipaddr':
					data = common.IPAddrInputDialog(default=data)
				else:
					data = None
			self._set(control, data)


	def _get(self, control):
		data = None
		if control is not None:
			data = control.getLabel()
			data = '' if data is None else data
			self.debug("Getting control label: %s" %str(data))
		return data


	def _set(self, control, data):
		if control is not None and data is not None:
			self.debug('Setting control label: %s' %str(data))
			control.setLabel(str(data))