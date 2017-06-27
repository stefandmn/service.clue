#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import abc
from runners import *
import lib.Scheduler as scheduler

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc

class ClueService:
	RUNNERS = {}

	def __init__(self):
		# Start jobs according to the input parameters
		if len(sys.argv) <= 1:
			commons.debug('%s v%s has been started: %s' %(commons.AddonName(), commons.AddonVersion(), 'service'))
			# Check if it runs for the first time
			self.isRunningFirstTime()
			self.runScheduler()
		else:
			_code = str(sys.argv[1]).strip()
			commons.info('%s v%s has been started: %s' %(commons.AddonName(), commons.AddonVersion(), _code))
			_runner = self.getRunner(_code)
			if _runner is not None:
				commons.debug("Starting service runner: %s" %str(_runner))
				_runner.run()
			else:
				commons.error("Unknown service runner: %s" %_code)
		commons.debug('%s v%s has been terminated' %(commons.AddonName(), commons.AddonVersion()))

	def getRunner(self, code):
		if not ClueService.RUNNERS:
			for cls in ClueServiceRunner.__subclasses__():
				mymodule = __import__(cls.__module__)
				myclass = getattr(mymodule, cls.__name__)
				myinstance = myclass()
				ClueService.RUNNERS[myinstance.code()] = myinstance
		if ClueService.RUNNERS.has_key(code):
			return ClueService.RUNNERS[code]
		else:
			return None

	def isRunningFirstTime(self):
		# check if first run
		addondata = xbmc.translatePath("special://profile/addon_data/%s/" %commons.AddonId())
		firstlock = os.path.join(addondata, '.firstrun')
		if not os.path.isfile(firstlock):
			if not os.path.exists(addondata):
				os.mkdir(addondata)
			# Run plugin for configuration
			commons.notice("Runing for the first time and start Clue Plugin to review and update default system configuration")
			xbmc.executebuiltin('XBMC.RunScript(plugin.clue)')
			open(firstlock, 'w').close()

	def runScheduler(self):
		cron = scheduler.SchedulerManager()
		cron.start()


class ClueServiceRunner(object):
	__metaclass__ = abc.ABCMeta

	def __repr__(self):
		return str(self.__class__) + " (" + str(self.code()) + ")"

	@abc.abstractmethod
	def code(self):
		return None
		pass

	@abc.abstractmethod
	def run(self):
		pass


if (__name__ == "__main__"):
	ClueService()
