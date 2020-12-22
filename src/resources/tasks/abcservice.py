# -*- coding: utf-8 -*-

import os
import abc
import common


class ServiceTask(object):
	__metaclass__ = abc.ABCMeta
	key = "service"
	HOME = os.environ['HOME']
	CONFIG_CACHE = os.environ.get('CONFIG_CACHE', '%s/.cache' % HOME)
	USER_CONFIG = os.environ.get('USER_CONFIG', '%s/.config' % HOME)


	def __init__(self):
		pass


	def __repr__(self):
		return str(self.__class__) + " (" + str(self.code()) + ")"


	@abc.abstractmethod
	def code(self):
		pass


	@abc.abstractmethod
	def run(self, *arg):
		pass


	def debug(self, txt):
		common.debug(txt, "task." + self.code())


	def info(self, txt):
		common.info(txt, "task." + self.code())


	def notice(self, txt):
		common.notice(txt, "task." + self.code())


	def warn(self, txt):
		common.warn(txt, "task." + self.code())


	def error(self, txt):
		common.error(txt, "task." + self.code())


	def _function(self, cmd, *args, **kwargs):
		if cmd is not None and cmd != '':
			if str(cmd).find('.') > 0:
				if str(cmd).startswith("self."):
					cmd = str(cmd).split(".")[1]
					return common.clscall(self, cmd, *args, **kwargs)
				else:
					cls = str(cmd).split(".")[0]
					cmd = str(cmd).split(".")[1]
					return common.clscall(cls, cmd, *args, **kwargs)
			else:
				return common.funcall(cmd, *args, **kwargs)
		else:
			return None


	def _process(self, cmd):
		if cmd is not None and cmd != '':
			return common.procexec(cmd)
		else:
			return None


	def any2int(self, v, error=False, none=True):
		return common.any2int(v, error=error,none=none)


	def any2float(self, v, error=False, none=True):
		return common.any2float(v, error=error,none=none)


	def any2str(self, v, error=False, none=True):
		return common.any2str(v, error=error,none=none)


	# Function: str2bool
	def any2bool(self, v, error=False, none=True):
		return common.any2bool(v, error=error,none=none)


	def translate(self, code):
		return common.translate(code)
