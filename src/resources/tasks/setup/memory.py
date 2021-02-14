# -*- coding: utf-8 -*-

import common
from resources.tasks.abcwindow import WindowTask


class Memory(WindowTask):
	key = "memory"


	def init(self, *args):
		self.setPropertyControlCallback(1211)
		self.setPropertyControlCallback(1212)
		self.setPropertyControlCallback(1213)


	def load(self):
		self.setPropertyControlValue(1211, self.sys.get_gpu_memorysplit())
		self.setPropertyControlValue(1212, self.sys.is_swap_enabled())
		self.setPropertyControlEnable(1213, self.sys.is_swap_enabled())
		self.setPropertyControlValue(1213, self.sys.get_swap_size())


	def onClick_1211(self):
		value = self.getPropertyControlValue(1211)
		if value is not None and value != '':
			self._lock()
			self.trace("Applying [%s] value for [%s] configuration property within %s file" % (str(value), self.sys.PROP_BOOT_GPU_MEM, self.sys.FILE_BOOT))
			self.sys.set_gpu_memorysplit(value)
			self.mark4reboot()
			self._unlock()


	def onClick_1212(self):
		value = self.any2bool(self.getPropertyControlValue(1212))
		if value is not None and value != '':
			self._lock()
			self.trace("Applying [%s] value for [%s] configuration property within %s file" %(str(value), self.sys.PROP_SWAP_ENABLED, self.sys.FILE_SWAP))
			self.sys.set_swap_enabled(value)
			self.setPropertyControlEnable(1213, self.sys.is_swap_enabled())
			self.mark4reboot()
			self._unlock()


	def onClick_1213(self):
		value = self.getPropertyControlValue(1213)
		if value is not None and value != '':
			self._lock()
			self.trace("Applying [%s] value for [%s] configuration property within %s file" %(str(value), self.sys.PROP_SWAP_SIZE, self.sys.FILE_SWAP))
			self.sys.set_swap_size(value)
			self.mark4reboot()
			self._unlock()
