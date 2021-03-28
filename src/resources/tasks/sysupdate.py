# -*- coding: utf-8 -*-

import common
from .abcservice import ServiceTask



class SystemUpdate(ServiceTask):
	key = "sysupdate"


	def __init__(self):
		self.silent = True
		ServiceTask.__init__(self)


	def run(self, *args):
		params = self.params(args)
		if "silent" in params:
			self.silent = self.any2bool(params['silent'])
		self.debug("*** TEST silent = %s, params = %s" %(self.silent, str(params)))
		common.setSkinProperty(10000, "SystemUpdate.Running", "true")
		update = self.sys.check_updates()
		if update is not None:
			common.DlgNotificationMsg(32903, time=7500)
			common.sleep(10)
			update = self.sys.doanload_updates()
			if update:
				if not self.silent:
					common.AskRestart(32904)
				else:
					self.notice("Reboot system to apply downloaded release update")
					#common.runBuiltinCommand("Reboot")
		common.setSkinProperty(10000, "SystemUpdate.Running")
