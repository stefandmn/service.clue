# -*- coding: utf-8 -*-


class AbstractRunner(object):
	def __init__(self):
		pass

	def run(self, provider, context=None):
		raise NotImplementedError()
