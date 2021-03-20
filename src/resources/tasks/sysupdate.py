# -*- coding: utf-8 -*-

import common
from .abcservice import ServiceTask



class SystemUpdater(ServiceTask):
	key = "sysupdate"


	def __init__(self):
		ServiceTask.__init__(self)


	def run(self, *arg):
		update = self.sys.check_updates()
		if update is not None:
			common.DlgNotificationMsg(32903, time=7500)
			common.sleep(10)
			update = self.sys.doanload_updates()
			if update:
				self.notice("Reboot system to apply downloaded release update")
				common.runBuiltinCommand("Reboot")
