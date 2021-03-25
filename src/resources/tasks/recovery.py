# -*- coding: utf-8 -*-

import common
from .abcservice import ServiceTask



class Recovery(ServiceTask):
	key = "recovery"


	def __init__(self):
		ServiceTask.__init__(self)
		self.mode = "backup"


	def _isrunnung(self):
		return self.any2bool(common.getSkinProperty(10000, "SystemRecovery.Running"))


	def run(self, *args):
		params = self.params(args)
		if "mode" in params:
			self.mode = params['mode'] if params['mode'] in ["backup", "restore"] else "backup"
		if not self._isrunnung():
			self.info("Starting system recovery process in %s mode" %self.mode)
			common.runBuiltinCommand("RunScript", "program.recovery", "mode=%s" %self.mode)
			while self._isrunnung():
				common.sleep()
			self.info("Ending system recovery process")
		else:
			self.warn("Recovery process is already running")