#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import abc
import lib.Commons as commons
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
			commons.info('%s v%s has been started: %s' %(commons.AddonName(),commons.AddonVersion(),'service'))
			# Check if it runs for the first time
			self.isRunningFirstTime()
			self.runScheduler()
		else:
			_code = str(sys.argv[1]).strip()
			commons.info('%s v%s has been started: %s' %(commons.AddonName(),commons.AddonVersion(),_code))
			_runner = self.getRunner(_code)
			if _runner is not None:
				commons.debug("Starting service runner: %s" %str(_runner))
				_runner.run()
			else:
				commons.error("Unknown service runner: %s" %_code)
		commons.debug('%s v%s has been terminated' %(commons.AddonName(),commons.AddonVersion()))

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


class MusicLibraryUpdate(ClueServiceRunner):

	def code(self):
		return "musiclib"

	def run(self):
		if commons.setting("musiclib"):
			if not xbmc.getCondVisibility('Library.IsScanningMusic'):
				xbmc.executebuiltin("UpdateLibrary(music)")
				xbmc.sleep(1500)
				if commons.setting("musiclib_clean"):
					while xbmc.getCondVisibility('Library.IsScanningVideo'):
						xbmc.sleep(500)
					xbmc.executebuiltin("CleanLibrary(music)")
				commons.info("Update of music library have been executed successfully", "MusicUpdate")
			else:
				commons.warn("Music library is currently scanned, so the update procedure will be skipped this time", "MusicUpdate")


class VideoLibraryUpdate(ClueServiceRunner):

	def code(self):
		return "videolib"

	def run(self):
		if commons.setting("videolib"):
			if not xbmc.getCondVisibility('Library.IsScanningVideo'):
				xbmc.executebuiltin("UpdateLibrary(video)")
				xbmc.sleep(1500)
				if commons.setting("videolib_clean"):
					while xbmc.getCondVisibility('Library.IsScanningVideo'):
						xbmc.sleep(500)
					xbmc.executebuiltin("CleanLibrary(video)")
				commons.info("Update of video library have been executed successfully", "VideoUpdate")
			else:
				commons.warn("Video library is currently scanned, so the update procedure will be skipped this time", "VideoUpdate")


class ClueSystemUpdate(ClueServiceRunner):

	def code(self):
		return "system"

	def run(self):
		if commons.setting("system"):
			(_status,_content) = commons.procexec("/opt/clue/bin/setup -g update")
			if _status and commons.any2int(_content.strip()) == 0:
				commons.NotificationMsg(commons.translate(32010))
				_cmd = "/opt/clue/bin/setup -s update -p"
				_opt = "-a" if commons.setting("system_osupgrade") else ""
				(_status,_content) = commons.procexec("%s %s" %(_cmd,_opt))
				# Run system integrity procedure
				if _status:
					if commons.setting("system_osintegrity"):
						_cmd = "/opt/clue/bin/setup -s update -s"
						(_status,_content) = commons.procexec(_cmd)
				if _status:
					commons.NotificationMsg(commons.translate(32011))
				else:
					commons.NotificationMsg(commons.translate(32012))
			else:
				commons.warn("System update is currently running, so the update procedure will be skipped this time", "SystemUpdate")


if (__name__ == "__main__"):
	ClueService()
