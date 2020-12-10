# -*- coding: utf-8 -*-

import sys
import common
from .abstract import ServiceRunner

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc

if hasattr(sys.modules["__main__"], "xbmcgui"):
	xbmcgui = sys.modules["__main__"].xbmcgui
else:
	import xbmcgui



class SetLabel(ServiceRunner):

	def code(self):
		return "setlabel"

	def run(self, *arg):
		params = dict(arg.split("=") for arg in sys.argv[0].split("&"))
		dialog = params.get("dialog")
		window = params.get("window")
		field = params.get("field")
		if dialog is None or dialog == '' or (dialog.tolower() != 'string' and dialog.tolower() != 'number'):
			dialog = 'string'
			common.debug('Using dialog type: %s' %str(dialog))
		if window is None or window == '':
			window = xbmcgui.getCurrentWindowId()
			if window is None:
				window = xbmcgui.getCurrentWindowDialogId()
			common.debug("Detected window id: %s" %str(window))
		if window is not None:
			window = xbmcgui.Window(int(window))
		if dialog == 'string':
			label = common.StringInputDialog()
		elif dialog == 'number':
			label = common.NumberInputDialog()
		if window is not None and field is not None and field != '':
			common.debug('Setting label of control id [%s] with text: %s' %(str(field), str(label)))
			control = window.getControl(field)
			control.setLabel(str(label))