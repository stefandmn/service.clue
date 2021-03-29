# -*- coding: utf-8 -*-

import abc
import common
from resources.appliance import Clue



class ServiceTask(object):
	__metaclass__ = abc.ABCMeta
	key = "service"
	sys = Clue()

	def __init__(self):
		pass


	def __repr__(self):
		return str(self.__class__) + " (" + str(self.code()) + ")"


	def code(self):
		return self.key


	@abc.abstractmethod
	def run(self, *args):
		pass


	def trace(self, txt):
		self.sys.trace(txt, "task." + self.code())


	def debug(self, txt):
		self.sys.debug(txt, "task." + self.code())


	def info(self, txt):
		self.sys.info(txt, "task." + self.code())


	def notice(self, txt):
		self.sys.notice(txt, "task." + self.code())


	def warn(self, txt):
		self.sys.warn(txt, "task." + self.code())


	def error(self, txt):
		self.sys.error(txt, "task." + self.code())


	def caller(self, cmd, *args, **kwargs):
		if cmd is not None and cmd != '':
			if str(cmd).find('.') > 0:
				if str(cmd).startswith("self."):
					cmd = str(cmd).split(".")[1]
					return self.method(self, cmd, *args, **kwargs)
				else:
					cls = str(cmd).split(".")[0]
					cmd = str(cmd).split(".")[1]
					return self.method(cls, cmd, *args, **kwargs)
			else:
				return self.function(cmd, *args, **kwargs)
		else:
			return None


	def method(self, cls, mtd, *args, **kwargs):
		return self.sys.method(cls, mtd, *args, **kwargs)


	def function(self, fnc, *args, **kwargs):
		return self.sys.function(fnc, *args, **kwargs)


	def process(self, cmd):
		return self.sys.process(cmd)


	def any2int(self, v, error=False, none=True):
		return self.sys.any2int(v, error=error, none=none)


	def any2float(self, v, error=False, none=True):
		return self.sys.any2float(v, error=error, none=none)


	def any2str(self, v, error=False, none=True):
		return self.sys.any2str(v, error=error, none=none)


	def any2bool(self, v, error=False, none=True):
		return self.sys.any2bool(v, error=error, none=none)


	def translate(self, code):
		return self.sys.translate(code)


	def params(self, args):
		params = {}
		for arg in args:
			if arg.startswith('?'):
				arg = arg[1:]
			vars = common.urlparsequery(arg)
			if vars is not None and len(vars) > 0:
				for var in vars:
					params[var[0]] = var[1]
		return params
