# -*- coding: utf-8 -*-

from resources.tasks.abcwindow import WindowTask


class FileSharing(WindowTask):
	key = "samba"


	def init(self, *args):
		self._changed = False
		self.setPropertyControlCallback(1210)
		self.setPropertyControlCallback(1211)
		self.setPropertyControlCallback(1212)
		self.setPropertyControlCallback(1213)
		self.setPropertyControlCallback(1214)
		self.setPropertyControlCallback(1215)
		self.setPropertyControlCallback(1216)
		self.setPropertyControlCallback(1217)


	def load(self):
		_status = self.sys.get_appservice_status("smbd", "samba") and self.sys.get_appservice_status("nmbd", "samba")
		self.setPropertyControlValue(1210, _status)
		self._setstate(_status)
		self.setPropertyControlValue(1211, self.sys.get_appservice_option("samba", "SAMBA_WORKGROUP"))
		self.setPropertyControlValue(1212, self.sys.get_appservice_option("samba", "SAMBA_USERNAME"))
		self.setPropertyControlValue(1213, self.sys.get_appservice_option("samba", "SAMBA_PASSWORD"))
		self.setPropertyControlValue(1214, self.sys.get_appservice_option("samba", "SAMBA_SECURE"))
		self.setPropertyControlValue(1215, self.sys.get_appservice_option("samba", "SAMBA_AUTOSHARE"))
		self.setPropertyControlValue(1216, self.sys.get_appservice_option("samba", "SAMBA_MINPROTOCOL"))
		self.setPropertyControlOptionData(1216, ["SMB1", "SMB2", "SMB3"])
		self.setPropertyControlValue(1217, self.sys.get_appservice_option("samba", "SAMBA_MAXPROTOCOL"))
		self.setPropertyControlOptionData(1217, ["SMB1", "SMB2", "SMB3"])


	def onClick_1210(self):
		value = self.any2bool(self.getPropertyControlValue(1210))
		self.debug("Applying [samba] services status: %s" % str(value))
		_status, _output = self.sys.set_appservice_status("smbd", value, conf="samba")
		if _status:
			_status, _output = self.sys.set_appservice_status("nmbd", value, conf="samba")
			if _status:
				self._lock()
				self.sys.wait(5)
				_status = self.sys.get_appservice_status("smbd", "samba") and self.sys.get_appservice_status("nmbd", "samba")
				self.setPropertyControlValue(1210, _status)
				self._setstate(_status)
				self._setchanged(False)
				self._unlock()
			else:
				self.DlgNotificationMsg(self.translate(31992) % _output)
		else:
			self.DlgNotificationMsg(self.translate(31992) % _output)


	def onClick_1211(self):
		value = self.getPropertyControlValue(1211)
		self.sys.set_appservice_option("samba", "SAMBA_WORKGROUP", value, quote=True)
		self._setchanged()


	def onClick_1212(self):
		value = self.getPropertyControlValue(1212)
		self.sys.set_appservice_option("samba", "SAMBA_USERNAME", value, quote=True)
		self._setchanged()


	def onClick_1213(self):
		value = self.getPropertyControlValue(1213)
		self.sys.set_appservice_option("samba", "SAMBA_PASSWORD", value, quote=True)
		self._setchanged()


	def onClick_1214(self):
		value = self.any2bool(self.getPropertyControlValue(1214))
		self.sys.set_appservice_option("samba", "SAMBA_SECURE", value, quote=True)
		self._setchanged()


	def onClick_1215(self):
		value = self.any2bool(self.getPropertyControlValue(1215))
		self.sys.set_appservice_option("samba", "SAMBA_AUTOSHARE", value, quote=True)
		self._setchanged()


	def onClick_1216(self):
		value = self.getPropertyControlValue(1216)
		self.sys.set_appservice_option("samba", "SAMBA_MINPROTOCOL", value, quote=True)
		self._setchanged()


	def onClick_1217(self):
		value = self.getPropertyControlValue(1217)
		self.sys.set_appservice_option("samba", "SAMBA_MAXPROTOCOL", value, quote=True)
		self._setchanged()


	def onClick_1218(self):
		self._lock()
		(_status, _output) = self.sys.restart_sysservice("smbd")
		if not _status:
			self.DlgNotificationMsg(self.translate(31993) % _output)
		else:
			(_status, _output) = self.sys.restart_sysservice("nmbd")
			if not _status:
				self.DlgNotificationMsg(self.translate(31993) % _output)
			else:
				self.sys.wait(5)
				__status = self.sys.get_appservice_status("smbd", "samba") and self.sys.get_appservice_status("nmbd", "samba")
				self.setPropertyControlValue(1210, _status)
				self._setstate(_status)
				self._setchanged(False)
		self._unlock()


	def _setstate(self, status=True):
		if status:
			self.setPropertyControlEnable(1211)
			self.setPropertyControlEnable(1212)
			self.setPropertyControlEnable(1213)
			self.setPropertyControlEnable(1214)
			self.setPropertyControlEnable(1215)
			self.setPropertyControlEnable(1216)
			self.setPropertyControlEnable(1217)
		else:
			self.setPropertyControlDisable(1211)
			self.setPropertyControlDisable(1212)
			self.setPropertyControlDisable(1213)
			self.setPropertyControlDisable(1214)
			self.setPropertyControlDisable(1215)
			self.setPropertyControlDisable(1216)
			self.setPropertyControlDisable(1217)


	def _setchanged(self, change=True):
		if self.sys.get_appservice_status("smbd", "samba"):
			self.setProperty("Samba.Restart", str(change).lower())
