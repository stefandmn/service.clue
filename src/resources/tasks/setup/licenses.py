# -*- coding: utf-8 -*-


from resources.tasks.abcwindow import WindowTask


class Licenses(WindowTask):
	key = "licenses"


	def init(self, *args):
		self.setPropertyControlCallback(1201)
		self.setPropertyControlCallback(1202)


	def load(self):
		(mpg2, wvc1) = self.sys.get_licenses()
		self.setPropertyControlValue(1201, mpg2)
		self.setPropertyControlValue(1202, wvc1)


	def onClick_1201(self):
		value = self.getPropertyControlValue(1201)
		self._lock()
		self.trace("Applying [%s] value for [%s] configuration property within %s file" %(str(value), self.sys.PROP_BOOT_MPG2, self.sys.FILE_BOOT))
		self.sys.set_mpg2_license(value)
		self.mark4reboot()
		self._unlock()


	def onClick_1202(self):
		value = self.getPropertyControlValue(1202)
		self._lock()
		self.trace("Applying [%s] value for [%s] configuration property within %s file" %(str(value), self.sys.PROP_BOOT_WVC1, self.sys.FILE_BOOT))
		self.sys.set_wvc1_licenses(value)
		self.mark4reboot()
		self._unlock()
