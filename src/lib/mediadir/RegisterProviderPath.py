# -*- coding: utf-8 -*-


class RegisterProviderPath(object):
	def __init__(self, re_path):
		self._media_re_path = re_path

	def __call__(self, func):
		def wrapper(*args, **kwargs):
			# only use a wrapper if you need extra code to be run here
			return func(*args, **kwargs)
		wrapper.media_re_path = self._media_re_path
		return wrapper
