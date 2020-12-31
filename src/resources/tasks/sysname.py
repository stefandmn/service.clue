# -*- coding: utf-8 -*-


from .abcwindow import WindowTask


class SystemName(WindowTask):
	key = "sysname"


	def init(self, *args):
		self.setPropertyControlLabel(1201, 31903)
		self.setPropertyControlValue(1202, True)


	def load(self):
		data = self.sys.get_hostname()
		self.debug("Found host name: %s" % str(data))
		self.setPropertyControlValue(1201, data)


	def onClick_1201(self):
		self._lock()
		name = self.getPropertyControlValue(1201)
		sync = self.getPropertyControlValue(1202)
		if name is not None:
			if self.any2bool(sync):
				self.sys.set_identity(name)
			else:
				self.sys.set_hostname(name)
		self._unlock()


	def onClick_1202(self):
		sync = self.getPropertyControlValue(1202)
		if self.any2bool(sync):
			self.setPropertyControlLabel(1201, 31903)
		else:
			self.setPropertyControlLabel(1201, 31912)