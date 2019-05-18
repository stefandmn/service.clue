# -*- coding: utf-8 -*-

import abc
import urlparse



class ServiceRunner(object):
	__metaclass__ = abc.ABCMeta


	def __repr__(self):
		return str(self.__class__) + " (" + str(self.code()) + ")"


	@abc.abstractmethod
	def code(self):
		return None
		pass


	@abc.abstractmethod
	def run(self, *arg):
		pass


	def input(self, *args):
		params = {}
		if len(args) > 1:
			for i in args:
				arg = i
				if arg.startswith('?'):
					arg = arg[1:]
				params.update(dict(urlparse.parse_qsl(arg)))
		return params
