# -*- coding: utf-8 -*-


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
		self.setPropertyControlOptionData(1203, self.sys.get_overclocking_profiles())
		self.setPropertyControlValue(1203, self.sys.get_currentoverclocking_profile())


	def onClick_1201(self):
		value = self.getPropertyControlValue(1201)
		if value is not None and value != '':
			self._lock()
			self.trace("Applying [%s] value for [%s] configuration property within %s file" %(str(value), self.sys.PROP_GPU_MEM, self.sys.FILE_BOOT_CONFIG))
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