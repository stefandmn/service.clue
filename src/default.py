# -*- coding: utf-8 -*-

import os
from runners import *
from lib.Scheduler import Scheduler

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc

if hasattr(sys.modules["__main__"], "xbmcgui"):
	xbmcgui = sys.modules["__main__"].xbmcgui
else:
	import xbmcgui


class ServiceSettings(xbmc.Monitor):
	updateSettingsMethod = None

	def __init__(self, *args, **kwargs):
		xbmc.Monitor.__init__(self)
		self.updateSettingsMethod = kwargs['updateSettingsMethod']

	def onSettingsChanged(self):
		commons.debug("Settings have been updated and will trigger re-loading of scheduler jobs", "ServiceSettings")
		self.updateSettingsMethod()


class ClueService:
	WEEKDAYS = ['monday', "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
	JOBNAMES = [ "sysupdater", "libupdater", "libcleaner", "sysbackup", "custom1", "custom2", "custom3", "custom4", "custom5", "custom6", "custom7", "custom8", "custom9", "custom10"]
	RUNNERS = {}

	def __init__(self):
		# Start jobs according to the input parameters
		if len(sys.argv) <= 1:
			commons.debug('%s v%s has been started: %s' %(commons.AddonName(), commons.AddonVersion(), 'service'))
			# Check if it runs for the first time
			self.isFirstTimeRunning()
			self.initScheduler()
		else:
			_code = str(sys.argv[1]).strip()
			commons.info('%s v%s has been started: %s' %(commons.AddonName(), commons.AddonVersion(), _code))
			_runner = self.getRunner(_code)
			if _runner is not None:
				commons.debug("Starting service runner: %s" %str(_runner))
				_runner.run(*sys.argv[2::])
			else:
				commons.error("Unknown service runner: %s" %_code)
		commons.debug('%s v%s has been terminated' %(commons.AddonName(), commons.AddonVersion()))

	def getRunner(self, code):
		if not ClueService.RUNNERS:
			for cls in ServiceRunner.__subclasses__():
				runnerInstance = cls()
				ClueService.RUNNERS[runnerInstance.code()] = runnerInstance
		if ClueService.RUNNERS.has_key(code):
			return ClueService.RUNNERS[code]
		else:
			return None

	def isFirstTimeRunning(self):
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

	def initScheduler(self):
		infoFlag = commons.any2bool(xbmc.getInfoLabel("Window(10000).Property(SchedulerService)"))
		if not infoFlag:
			xbmcgui.Window(10000).setProperty("SchedulerService", "true")
			self.settings = ServiceSettings(updateSettingsMethod=self.setupScheduler)
			self.scheduler = Scheduler()
			self.setupScheduler()
			self.startScheduler()
		else:
			commons.notice("Service component is already running!")

	def setupScheduler(self):
		self.scheduler.removeAll()
		self.loadScheduler()

	def startScheduler(self):
		while not xbmc.abortRequested:
			self.scheduler.run()
			xbmc.sleep(1000)

	def loadScheduler(self):
		commons.debug("Loading scheduler setting..")
		for jobname in self.JOBNAMES:
			job = None
			cfg = {
					"enabled": commons.setting(jobname),
					"cycle": commons.setting(jobname + "_cycle"),	# cycles: Weekly(0), Daily(1), Hourly(2), Minutes(3)
					"script": commons.setting(jobname + "_script"),
					"type": commons.setting(jobname + "_type"),		# script, addon, plugin, command, process, json
					"day": commons.setting(jobname + "_day"),
					"time": commons.setting(jobname + "_time"),
					"interval": commons.setting(jobname + "_interval")}
			cfg["day"] = self.WEEKDAYS[cfg["day"]] if cfg["day"] >= 0 else -1
			# Adapt job script
			if jobname == "sysupdater":
				cfg["script"] = "RunScript(%s, %s, %s, %s)" %(commons.AddonId(), jobname, commons.getSetting(jobname + "_osupgrade"), commons.getSetting(jobname + "_osintegrity"))
				cfg["type"] = "script"
			elif jobname == "libupdater":
				cfg["script"] = "RunScript(%s, %s, %s, %s)" %(commons.AddonId(), jobname, commons.getSetting(jobname + "_music"), commons.getSetting(jobname + "_video"))
				cfg["type"] = "script"
			elif jobname == "libcleaner":
				cfg["script"] = "RunScript(%s, %s, %s, %s)" %(commons.AddonId(), jobname, commons.getSetting(jobname + "_music"), commons.getSetting(jobname + "_video"))
				cfg["type"] = "script"
			elif jobname == "sysbackup":
				cfg["script"] = "RunScript(script.backuprestore, mode=backup)"
				cfg["type"] = "script"
			# Create job instance
			if cfg["enabled"] and cfg["script"] is not None and cfg["script"] != '':
				if cfg["cycle"] == 0:
					job = self.scheduler.newJob(jobname).every(cfg["interval"]).weeks.weekday(cfg["day"]).at(cfg["time"])
				elif cfg["cycle"] == 1:
					job = self.scheduler.newJob(jobname).every(cfg["interval"]).days.at(cfg["time"])
				elif cfg["cycle"] == 2:
					job = self.scheduler.newJob(jobname).every(cfg["interval"]).hours
				elif cfg["cycle"] == 3:
					job = self.scheduler.newJob(jobname).every(cfg["interval"]).minutes
				# Apply job script
				if job is not None and cfg["script"]:
					job.setScript(cfg["script"])
					job.setType(cfg["type"])
					commons.debug("Creating job: %s" %str(job))
				elif job is not None and not cfg["script"]:
					commons.error("Job '%s' is removed because no script has been configured to run" %jobname)
					self.scheduler.remove(job)
				else:
					commons.error("Error creating job based on configuration: %s" %jobname)
			else:
				commons.debug("Job '%s' is not enabled" %jobname)


if (__name__ == "__main__"):
	ClueService()
