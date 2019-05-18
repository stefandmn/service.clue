# -*- coding: utf-8 -*-

import commons
from abstract import ServiceRunner



class SystemUpdater(ServiceRunner):
	def __init__(self):
		self.osupgrade = False
		self.integrity = False


	def code(self):
		return "sysupdate"


	def detect(self, arg):
		if arg is not None and len(arg) == 1:
			if str(arg[0]).strip().lower() in ('upgrade', 'osupgrade'):
				self.osupgrade = True
			elif str(arg[0]).strip().lower() in ('integrity', 'osintegrity'):
				self.integrity = True
			else:
				self.osupgrade = commons.any2bool(arg[0])
		if arg is not None and len(arg) >= 2:
			self.osupgrade = commons.any2bool(arg[0])
			self.integrity = commons.any2bool(arg[1])


	def run(self, *arg):
		self.detect(arg)
		(_status, _content) = commons.procexec("/opt/clue/bin/setup -g update -s")
		if _status and commons.any2int(_content.strip()) == 0:
			commons.NotificationMsg(commons.translate(32010))
			_cmd = "/opt/clue/bin/setup -s update -p"
			_opt = "all" if self.osupgrade else ""
			(_status, _content) = commons.procexec("%s %s" % (_cmd, _opt))
			# Run system integrity procedure
			if _status and self.integrity:
				_cmd = "/opt/clue/bin/setup -s update -s"
				(_status, _content) = commons.procexec(_cmd)
			if _status:
				commons.NotificationMsg(commons.translate(32011))
			else:
				commons.NotificationMsg(commons.translate(32012))
		else:
			commons.warn("System update is currently running, so the update procedure will be skipped this time", "SystemUpdate")
