# -*- coding: utf-8 -*-

import xbmcgui
from resources.lib.mediadir.AbstractProgressDialog import AbstractProgressDialog


class ClueProgressDialog(AbstractProgressDialog):

	def __init__(self, heading, text):
		AbstractProgressDialog.__init__(self, 100)
		self._dialog = xbmcgui.DialogProgress()
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
			self._dialog.update(position, text)
		else:
			self._dialog.update(position)
		pass

	def isAborted(self):
		return self._dialog.iscanceled()
