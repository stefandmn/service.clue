# -*- coding: utf-8 -*-

from resources.tasks.abcwindow import WindowTask


class SystemAccess(WindowTask):
	key = "sysaccess"
	SSH_SERVICENAME = "sshd"
	SSH_PROP_DISABLEPWAUTH = "SSHD_DISABLE_PW_AUTH"


	def init(self, *args):
		self.setPropertyControlCallback(1201)
		self.setPropertyControlCallback(1202)
		self.setPropertyControlCallback(1203)
		sshd_status = self.sys.get_appservice_status(self.SSH_SERVICENAME)
		sshd_disablepasswd = self.sys.get_appservice_option(self.SSH_SERVICENAME, self.SSH_PROP_DISABLEPWAUTH)
		self.setPropertyControlValue(1202, sshd_status)
		self.setPropertyControlEnable(1203, sshd_status)
		self.setPropertyControlValue(1203, self.any2bool(sshd_disablepasswd))


	def onClick_1201(self):
		try:
			pwd = self.getPropertyControlValue(1201)
			self.trace("Get current password: %s" %pwd)
			result = self.sys.check_root_access(pwd)
			if result:
				self.NotificationMsg(self.translate(31914), time=5000)
				passwd1 = self.StringInputDialog(title=self.translate(31910), hidden=True)
				passwd2 = self.StringInputDialog(title=self.translate(31911), hidden=True)
				result = self.sys.set_root_password(passwd1, passwd2)
				if result:
					self.NotificationMsg(self.translate(31915), time=5000)
		except BaseException as be:
			self.DlgNotificationMsg(str(be))


	def onClick_1202(self):
		status = self.any2bool(self.getPropertyControlValue(1202))
		sysinfo = self.sys.get_sysservice_status(self.SSH_SERVICENAME)
		appinfo = self.sys.get_appservice_status(self.SSH_SERVICENAME)
		self.trace("SSH service has been %s, currently the service is %s, and is configured as %s service" %("enabled" if not status else "disabled", "running" if sysinfo else "stopped", "enabled" if appinfo else "disabled"))
		if status and (not sysinfo or not appinfo):
			if not appinfo:
				self.sys.enable_appservice(self.SSH_SERVICENAME)
			if not sysinfo:
				self.sys.start_sysservice(self.SSH_SERVICENAME)
		elif status and sysinfo and appinfo:
			self.DlgNotificationMsg(self.translate(32900))
		elif not status and (sysinfo or appinfo):
			if appinfo:
				self.sys.disable_appservice(self.SSH_SERVICENAME)
			if appinfo:
				self.sys.stop_sysservice(self.SSH_SERVICENAME)
		elif not status and not sysinfo and not appinfo:
			self.DlgNotificationMsg(self.translate(32901))
		self.setPropertyControlEnable(1203, status)


	def onClick_1203(self):
		status = self.any2bool(self.getPropertyControlValue(1203))
		appinfo = self.sys.get_appservice_status(self.SSH_SERVICENAME)
		self.debug("SSH service configuration to disable password authentication has been %s, taking into account the service is %s" %("enabled" if status else "disabled", "enabled" if appinfo else "disabled"))
		if appinfo:
			self.sys.set_appservice_option(self.SSH_SERVICENAME, self.SSH_PROP_DISABLEPWAUTH, str(status).lower())
		else:
			self.DlgNotificationMsg(self.translate(32902))
