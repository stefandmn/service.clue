# -*- coding: utf-8 -*-


class AbstractContextUI(object):
	def __init__(self):
		pass

	def createProgressDialog(self, heading, text=None, background=False):
		raise NotImplementedError()

	def getSkinId(self):
		raise NotImplementedError()

	def onKeyboardInput(self, title, default='', hidden=False):
		raise NotImplementedError()

	def onNumericInput(self, title, default=''):
		raise NotImplementedError()

	def onYesNoInput(self, title, text):
		raise NotImplementedError()

	def onOk(self, title, text):
		raise NotImplementedError()

	def onRemoveContent(self, content_name):
		raise NotImplementedError()

	def onSelect(self, title, items=[]):
		raise NotImplementedError()

	def openSettings(self):
		raise NotImplementedError()

	def showNotification(self, message, header='', image_uri='', time_milliseconds=5000):
		raise NotImplementedError()

	# Needs to be implemented by a mock for testing or the real deal. This will refresh the current container or list.
	def refreshContainer(self):
		raise NotImplementedError()

	def showBusyDialog(self):
		raise NotImplementedError()

	def closeBusyDialog(self):
		raise NotImplementedError()