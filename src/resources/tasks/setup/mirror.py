# -*- coding: utf-8 -*-

from resources.tasks.abcwindow import WindowTask


class RemoteScreen(WindowTask):
	key = "mirror"


	def init(self, *args):
		self.setPropertyControlCallback(1210)
		self.setPropertyControlCallback(1211)
		self.setPropertyControlCallback(1212)
		self.setPropertyControlCallback(1213)
		self.setPropertyControlCallback(1214)
		self.setPropertyControlCallback(1215)
		self.setPropertyControlCallback(1216)
		self._setchanged(False)


	def load(self):
		self.setPropertyControlValue(1210, self.sys.get_appservice_status("mirror"))
		self.setPropertyControlValue(1211, self.sys.get_appservice_option("mirror", "port"))
		self.setPropertyControlValue(1212, self.sys.get_appservice_option("mirror", "framerate"))
		self.setPropertyControlValue(1213, self.sys.get_appservice_option("mirror", "password"))
		self.setPropertyControlValue(1214, self.sys.get_appservice_option("mirror", "fullscreen"))
		self.setPropertyControlValue(1215, self.sys.get_appservice_option("mirror", "downscale"))
		self.setPropertyControlValue(1216, self.sys.get_appservice_option("mirror", "multi-threaded"))


	def onClick_1210(self):
		value = self.any2bool(self.getPropertyControlValue(1210))
		self.debug("Applying [mirror] service status: %s" % str(value))
		_status, _output = self.sys.set_appservice_status("mirror", value)
		if _status:
			self._lock()
			self.sys.wait(3)
			self.setPropertyControlValue(1210, self.sys.get_appservice_status("mirror"))
			self._setchanged(False)
			self._unlock()
		else:
			self.DlgNotificationMsg(self.translate(31992) % _output)


	def onClick_1211(self):
		value = self.getPropertyControlValue(1211)
		self.sys.set_appservice_option("mirror", "port", value, beautify=True)
		self._setchanged()


	def onClick_1212(self):
		value = self.getPropertyControlValue(1212)
		self.sys.set_appservice_option("mirror", "framerate", value, beautify=True)
		self._setchanged()


	def onClick_1213(self):
		value = self.getPropertyControlValue(1213)
		self.sys.set_appservice_option("mirror", "password", value, beautify=True, quote=True)
		self._setchanged()


	def onClick_1214(self):
		value = self.any2bool(self.getPropertyControlValue(1214))
		self.sys.set_appservice_option("mirror", "fullscreen", str(value).lower(), beautify=True)
		self._setchanged()


	def onClick_1215(self):
		value = self.any2bool(self.getPropertyControlValue(1215))
		self.sys.set_appservice_option("mirror", "downscale", str(value).lower(), beautify=True)
		self._setchanged()


	def onClick_1216(self):
		value = self.any2bool(self.getPropertyControlValue(1216))
		self.sys.set_appservice_option("mirror", "multi-threaded", str(value).lower(), beautify=True)
		self._setchanged()


	def onClick_1217(self):
		self._lock()
		(_status, _output) = self.sys.restart_sysservice("mirror")
		if not _status:
			self.DlgNotificationMsg(self.translate(31993) %_output)
		else:
			self.sys.wait(3)
			_status = self.sys.get_appservice_status("mirror")
			self.setPropertyControlValue(1210, _status)
			self._setchanged(False)
		self._unlock()


	def _setchanged(self, change=True):
		if self.sys.get_appservice_status("mirror"):
			self.setProperty("Mirror.Restart", str(change).lower())
