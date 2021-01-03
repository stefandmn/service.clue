# -*- coding: utf-8 -*-

import abc
import sys
import common
from .abcservice import ServiceTask

if hasattr(sys.modules["__main__"], "xbmcgui"):
	xbmcgui = sys.modules["__main__"].xbmcgui
else:
	import xbmcgui


class GraphicTask(ServiceTask):
	__metaclass__ = abc.ABCMeta
	key = "graphic"


	def run(self, *args):
		params = dict(arg.split("=") for arg in sys.argv[2].split("&"))
		self.debug('Found parameters: %s' %str(params))
		self._dialog = params.get("dialog")
		self._dialog = 'string' if self._dialog is None or self._dialog == '' or (self._dialog.lower() != 'string' and self._dialog.lower() != 'number' and self._dialog.lower() != 'date' and self._dialog.lower() != 'time' and self._dialog.lower() != 'ipaddr' and self._dialog.lower() != 'select' and self._dialog.lower() != 'none') else self._dialog
		self.trace('Using dialog type: %s' % str(self._dialog))
		self._wid = params.get("window")
		self.trace('Using window id: %s' % str(self._wid))
		self._title = params.get("title")
		self.trace('Using window title: %s' % str(self._title))
		self._property = params.get("property")
		self.trace('Using window property: %s' % str(self._property))
		self._control = params.get("control")
		self.trace('Using window field: %s' % str(self._control))
		self._data = params.get("data")
		self.trace('Using data: %s' % str(self._data))
		self._default = params.get("default")
		self.trace('Using default input data: %s' % str(self._default))
		self._callback = params.get("callback")
		self.trace('Using callback data: %s' % str(self._callback))
		try:
			if self._wid is None:
				self._wid = xbmcgui.getCurrentWindowId() if self._wid is None else self._wid
				self._wid= xbmcgui.getCurrentWindowDialogId() if self._wid is None else self._wid
			self._window = xbmcgui.Window(self._wid)
			self.trace('Detected window id: %s' % str(self._wid))
		except BaseException as be:
			self.error("Error discovering window handler: %s" %str(be))
			self._window = None
		if self._window is not None and self._dialog != 'none':
			self._presetup()
			if self._dialog == 'string':
				self._data = common.StringInputDialog(title=self._title, default=self._default)
			elif self._dialog == 'number':
				self._data = common.NumberInputDialog(title=self._title, default=self._default)
			elif self._dialog == 'date':
				self._data = common.DateInputDialog(title=self._title, default=self._default)
			elif self._dialog == 'time':
				self._data = common.TimeInputDialog(title=self._title, default=self._default)
			elif self._dialog == 'ipaddr':
				self._data = common.IPAddrInputDialog(title=self._title, default=self._default)
			elif self._dialog == 'select':
				self._data = common.SelectDialog(title=self._title, default=self._default, options=self._data)
			else:
				self._data = None
			self._setup()
		else:
			if self._dialog != 'none':
				self.error("Window handler is unknown")
			else:
				self.debug("Process skipped due to rejected input dialog from XML window definition")
		# process callback process
		if self._callback is not None:
			common.runBuiltinCommand(self._callback, wait=True)


	@abc.abstractmethod
	def _presetup(self):
		pass


	@abc.abstractmethod
	def _setup(self):
		pass
