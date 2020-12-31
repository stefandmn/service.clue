# -*- coding: utf-8 -*-

from .abcwindow import WindowTask


class SystemAccess(WindowTask):
	key = "sysaccess"


	def init(self, *args):
		self.setPropertyControlCallback(2201)
		sshd_status = self.sys.get_appservice_status("sshd")
		sshd_disablepasswd = self.sys.get_appservice_option("sshd", "SSHD_DISABLE_PW_AUTH")
		self.setPropertyControlValue(2202, sshd_status)
		self.setPropertyControlEnable(2203, sshd_status)
		self.setPropertyControlValue(2203, self.any2bool(sshd_disablepasswd))


	def onClick_2201(self):
		try:
			pwd = self.getPropertyControlValue(2201)
			self.debug("Get current password: %s" %pwd)
			self.sys.check_root_access(pwd)
			self.DlgNotificationMsg(self.translate(31914))
			passwd1 = self.StringInputDialog(title=self.translate(31910), hidden=True)
			passwd2 = self.StringInputDialog(title=self.translate(31911), hidden=True)
			self.sys.set_root_password(passwd1, passwd2)
			self.DlgNotificationMsg(self.translate(31915))
		except BaseException as be:
			self.DlgNotificationMsg(str(be))

