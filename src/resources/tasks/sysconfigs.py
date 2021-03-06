# -*- coding: utf-8 -*-

import common
from .abcwindow import WindowTask


class SystemConfigs(WindowTask):
	key = "sysconfigs"


	def init(self, *args):
		self.setPropertyControlCallback(1201)
		self.setPropertyControlCallback(1202)
		self.setPropertyControlCallback(1203)
		self.setPropertyControlCallback(1204)
		self.setPropertyControlCallback(1205)
		self.setPropertyControlCallback(1206)
		self.setPropertyControlCallback(1207)
		self.setPropertyControlValue(1201, self.sys.get_gpu_memorysplit())
		self.setPropertyControlValue(1202, self.sys.get_turbomode())
		self.setPropertyControlEnable(1203, not self.sys.get_turbomode())
		self.setPropertyControlValue(1204, common.setting("recovery"))
		self.setPropertyControlValue(1205, common.setting("sysupdate"))
		self.setPropertyControlOptionData(1203, self.sys.get_overclocking_profiles())
		self.setPropertyControlValue(1203, self.sys.get_currentoverclocking_profile())


	def onClick_1201(self):
		value = self.getPropertyControlValue(1201)
		if value is not None and value != '':
			self._lock()
			self.trace("Applying [%s] value for [%s] configuration property within %s file" % (str(value), self.sys.PROP_BOOT_GPU_MEM, self.sys.FILE_BOOT))
			self.sys.set_gpu_memorysplit(value)
			self.mark4reboot()
			self._unlock()


	def onClick_1202(self):
		value = self.any2bool(self.getPropertyControlValue(1202))
		if value is not None and value != '':
			self._lock()
			self.trace("%s turbo mode" %("Applying" if value else "Removing"))
			self.sys.set_turbomode(value)
			self.setPropertyControlEnable(1203, not self.sys.get_turbomode())
			self.mark4reboot()
			self._unlock()


	def onClick_1203(self):
		value = self.getPropertyControlValue(1203)
		if value is not None and value != '':
			self._lock()
			self.trace("Applying [%s] overclocking profile" %str(value))
			self.sys.set_overclocking_profile(value)
			self.mark4reboot()
			self._unlock()


	def onClick_1204(self):
		value = self.getPropertyControlValue(1204)
		if self.any2bool(value):
			self.trace("Activating system recovery process to run in backup mode")
			common.setAddonSetting("service.clue", "recovery", True)
			common.setAddonSetting("service.clue", "recovery_type", "backup")
		else:
			common.setAddonSetting("service.clue", "recovery", False)


	def onClick_1205(self):
		value = self.getPropertyControlValue(1205)
		if self.any2bool(value):
			self.trace("Activating automatic system updates")
			common.setAddonSetting("service.clue", "sysupdate", True)
		else:
			common.setAddonSetting("service.clue", "sysupdate", False)


	def onClick_1206(self):
		if self.YesNoDialog(31946):
			pass
		else:
			self.warn("Reset Kodi to Default operation has been Cancelled")


	def onClick_1207(self):
		if self.YesNoDialog(31947):
			pass
		else:
			self.warn("Reset System to Default operation has been Cancelled")