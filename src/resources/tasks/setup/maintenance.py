# -*- coding: utf-8 -*-

import common
from resources.tasks.abcwindow import WindowTask


class Maintenance(WindowTask):
	key = "maintenance"


	def init(self, *args):
		self.setPropertyControlCallback(1211)
		self.setPropertyControlCallback(1212)
		self.setPropertyControlCallback(1213)
		self.setPropertyControlCallback(1214)
		self.setPropertyControlCallback(1215)
		self.setPropertyControlCallback(1216)


	def load(self):
		self.setPropertyControlValue(1211, common.setting("recovery"))
		self.setPropertyControlValue(1212, common.setting("sysupdate"))
		self.setPropertyControlValue(1213, self.sys.get_appservice_status("avahi-daemon", "avahi"))
		self.setPropertyControlValue(1214, self.sys.get_appservice_status("cron", "crond"))
		self.setPropertyControlEnable(1215)
		self.setPropertyControlEnable(1216)


	def onClick_1211(self):
		value = self.any2bool(self.getPropertyControlValue(1211))
		if value:
			self.debug("Activating system recovery process to run in backup mode")
			common.setAddonSetting("service.clue", "recovery", True)
			common.setAddonSetting("service.clue", "recovery_type", "backup")
		else:
			common.setAddonSetting("service.clue", "recovery", False)


	def onClick_1212(self):
		value = self.any2bool(self.getPropertyControlValue(1212))
		if value:
			self.debug("Activating automatic system updates")
			common.setAddonSetting("service.clue", "sysupdate", True)
		else:
			common.setAddonSetting("service.clue", "sysupdate", False)


	def onClick_1213(self):
		value = self.any2bool(self.getPropertyControlValue(1213))
		self.debug("Applying [avahi] service status: %s" % str(value))
		_status, _output = self.sys.set_appservice_status("avahi-daemon", value, "avahi")
		if _status:
			self.setPropertyControlValue(1213, self.sys.get_appservice_status("avahi-daemon", "avahi"))
		else:
			self.DlgNotificationMsg(self.translate(31994) % _output)


	def onClick_1214(self):
		value = self.any2bool(self.getPropertyControlValue(1214))
		self.debug("Applying [cron] service status: %s" % str(value))
		_status, _output = not self.sys.set_appservice_status("cron", value, "crond")
		if _status:
			self.setPropertyControlValue(1214, self.sys.get_appservice_status("cron", "crond"))
		else:
			self.DlgNotificationMsg(self.translate(31994) % _output)


	def onClick_1215(self):
		if self.YesNoDialog(31946):
			open("%s/reset_kodi" % self.sys.CACHE, 'a').close()
			self.mark4reboot()
			self.NotificationMsg(31948)
		else:
			self.warn("Soft reset operation has been Cancelled")


	def onClick_1216(self):
		if self.YesNoDialog(31947):
			open("%s/reset_clue" % self.sys.CACHE, 'a').close()
			self.mark4reboot()
			self.NotificationMsg(31949)
		else:
			self.warn("Hard reset operation has been Cancelled")
