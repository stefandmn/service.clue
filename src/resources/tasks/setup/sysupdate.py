# -*- coding: utf-8 -*-

import common
from resources.tasks.abcservice import ServiceTask



class SystemUpdater(ServiceTask):
	key = "sysupdate"


	def __init__(self):
		ServiceTask.__init__(self)
		self.osupgrade = False
		self.integrity = False


	def detect(self, arg):
		if arg is not None and len(arg) == 1:
			if str(arg[0]).strip().lower() in ('upgrade', 'osupgrade'):
				self.osupgrade = True
			elif str(arg[0]).strip().lower() in ('integrity', 'osintegrity'):
				self.integrity = True
			else:
				self.osupgrade = common.any2bool(arg[0])
		if arg is not None and len(arg) >= 2:
			self.osupgrade = common.any2bool(arg[0])
			self.integrity = common.any2bool(arg[1])


	def run(self, *arg):
		self.detect(arg)
		(_status, _content) = common.procexec("/opt/clue/bin/setup -g update -s")
		if _status and common.any2int(_content.strip()) == 0:
			common.NotificationMsg(common.translate(32010))
			_cmd = "/opt/clue/bin/setup -s update -p"
			_opt = "all" if self.osupgrade else ""
			(_status, _content) = common.procexec("%s %s" % (_cmd, _opt))
			# Run system integrity procedure
			if _status and self.integrity:
				_cmd = "/opt/clue/bin/setup -s update -s"
				(_status, _content) = common.procexec(_cmd)
			if _status:
				common.NotificationMsg(common.translate(32011))
			else:
				common.NotificationMsg(common.translate(32012))
		else:
			common.warn("System update is currently running, so the update procedure will be skipped this time", "SystemUpdate")
