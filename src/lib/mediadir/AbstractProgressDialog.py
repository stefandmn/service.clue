# -*- coding: utf-8 -*-


class AbstractProgressDialog(object):
	def __init__(self, total=100):
		self._total = int(total)
		self._position = 0

	def getTotal(self):
		return self._total

	def getPosition(self):
		return self._position

	def close(self):
		raise NotImplementedError()

	def setTotal(self, total):
		self._total = int(total)

	def update(self, steps=1, text=None):
		raise NotImplementedError()

	def isAborted(self):
		raise NotImplementedError()
