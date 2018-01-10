# -*- coding: utf-8 -*-

import sys
from mediadir.AbstractProgressDialog import AbstractProgressDialog

if hasattr(sys.modules["__main__"], "xbmcgui"):
	xbmcgui = sys.modules["__main__"].xbmcgui
else:
	import xbmcgui


class ClueProgressDialogBG(AbstractProgressDialog):

	def __init__(self, heading, text):
		AbstractProgressDialog.__init__(self, 100)
		self._dialog = xbmcgui.DialogProgressBG()
		self._dialog.create(heading, text)
		# simple reset because KODI won't do it :(
		self._position = 1
		self.update(steps=-1)

	def close(self):
		if self._dialog:
			self._dialog.close()
			self._dialog = None
		pass

	def update(self, steps=1, text=None):
		self._position += steps
		position = int(float(100.0 / self._total) * self._position)
		if isinstance(text, basestring):
			self._dialog.update(percent=position, message=text)
		else:
			self._dialog.update(percent=position)
		pass

	def isAborted(self):
		return False
