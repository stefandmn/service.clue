# -*- coding: utf-8 -*-

import common
from resources.tasks.abcwindow import WindowTask


class Overclocking(WindowTask):
	key = "overclocking"


	def init(self, *args):
		self.setPropertyControlCallback(1201)
		self.setPropertyControlCallback(1202)
		self.setPropertyControlOptionData(1202, self.sys.get_overclocking_profiles())
		self.setPropertyControlEnable(1202, not self.sys.get_turbomode())


	def load(self):
		self.setPropertyControlValue(1201, self.sys.get_turbomode())
		self.setPropertyControlValue(1202, self.sys.get_currentoverclocking_profile())


	def onClick_1201(self):
		value = self.any2bool(self.getPropertyControlValue(1201))
		if value is not None and value != '':
			self._lock()
			self.trace("%s turbo mode" %("Applying" if value else "Removing"))
			self.sys.set_turbomode(value)
			self.setPropertyControlEnable(1202, not self.sys.get_turbomode())
			self.mark4reboot()
			self._unlock()


	def onClick_1202(self):
		value = self.getPropertyControlValue(1202)
		if value is not None and value != '':
			self._lock()
			self.trace("Applying [%s] overclocking profile" %str(value))
			self.sys.set_overclocking_profile(value)
			self.mark4reboot()
			self._unlock()
