# -*- coding: utf-8 -*-


from .abcwindow import WindowTask


class SystemConfigs(WindowTask):
	key = "sysconfigs"
	BOOT_CONFIG = "/boot/config.txt"
	GPU_MEM = "gpu_mem"


	def init(self, *args):
		self.setPropertyControlCallback(1201)
		self.setPropertyControlValue(1201, self.sys.get_property(self.BOOT_CONFIG, self.GPU_MEM, 128))


	def onClick_1201(self):
		self._lock()
		value = self.getPropertyControlValue(1201)
		self.sys.remount_boot(True)
		self.sys.set_property(self.BOOT_CONFIG, self.GPU_MEM, value)
		self.sys.remount_boot(False)
		self._unlock()