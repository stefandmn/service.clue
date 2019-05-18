# -*- coding: utf-8 -*-

import os
from scheduler import *
from resources.runners import ServiceRunner

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
		commons.debug("Settings have been updated and will trigger re-loading of scheduler jobs", "service.Settings")
		self.updateSettingsMethod()



class ClueService:
	WEEKDAYS = ['monday', "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
	JOBNAMES = [ "sysupdate", "libupdate", "libclean", "sysbackup", "custom1", "custom2", "custom3", "custom4", "custom5", "custom6", "custom7", "custom8", "custom9", "custom10"]
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
			commons.info('%s v%s has been started: %s' %(commons.AddonName(), commons.AddonVersion(), _code), 'service')
			_runner = self.getRunner(_code)
			if _runner is not None:
				commons.debug("Starting service runner: %s" %str(_runner), 'service')
				_runner.run(*sys.argv[2::])
			else:
				commons.error("Unknown service runner: %s" %_code)
		commons.debug('%s v%s has been terminated' %(commons.AddonName(), commons.AddonVersion()), 'service')


	def readRunners(self):
		"""Detect all implemented and declared service runners and build up the corresponding dictionary"""
		self.RUNNERS.clear()
		for cls in ServiceRunner.__subclasses__():
			try:
				runner = cls()
				if not self.RUNNERS.has_key(runner.code()):
					self.RUNNERS[runner.code()] = runner
				else:
					commons.error("Invalid signature of service runner, it has the same id with another one: %s " %runner, 'service')
			except BaseException as be:
				commons.error('Unexpected error while reading [%s] service runner: %s' %(str(cls),str(be)), 'service')


	def getRunner(self, code):
		"""Returns the service runner having the specified signature """
		runner = None
		if not self.RUNNERS:
			self.readRunners()
		if code is not None and self.RUNNERS.has_key(code):
			runner = self.RUNNERS[code]
		return runner


	def isFirstTimeRunning(self):
		# check if first run
		addondata = xbmc.translatePath("special://profile/addon_data/%s/" %commons.AddonId())
		firstlock = os.path.join(addondata, '.firstrun')
		if not os.path.isfile(firstlock):
			if not os.path.exists(addondata):
				os.mkdir(addondata)
			open(firstlock, 'w').close()
			firstrun = threading.Thread(target=self._runFirstTime)
			firstrun.start()


	def _runFirstTime(self):
		xbmc.sleep(5000)
		commons.notice("Running for the first time and start Clue System Setup add-on to review and update default system configuration", 'service')
		xbmc.executebuiltin('XBMC.RunScript(program.clue)')


	def initScheduler(self):
		infoFlag = commons.any2bool(xbmc.getInfoLabel("Window(10000).Property(SystemSetup.SchedulerStatus)"))
		if not infoFlag:
			xbmcgui.Window(10000).setProperty("SystemSetup.SchedulerStatus", "true")
			self.settings = ServiceSettings(updateSettingsMethod=self.setupScheduler)
			self.scheduler = Scheduler()
			self.setupScheduler()
			self.startScheduler()
		else:
			commons.notice("Service component is already running!", 'service')


	def setupScheduler(self):
		self.scheduler.removeAll()
		self.loadScheduler()


	def startScheduler(self):
		while not xbmc.abortRequested:
			self.scheduler.run()
			xbmc.sleep(1000)


	def loadScheduler(self):
		commons.debug("Loading scheduler settings..", 'service')
		for jobname in self.JOBNAMES:
			job = None
			cfg = {
					"enabled": commons.setting(jobname),
					"cycle": commons.setting(jobname + "_cycle"),		# cycles: Weekly(0), Daily(1), Hourly(2), Minutes(3)
					"script": commons.setting(jobname + "_script"),
					"type": commons.setting(jobname + "_type"),			# script, addon, plugin, command, process, json
					"day": commons.setting(jobname + "_day"),
					"time": commons.setting(jobname + "_time"),
					"interval": commons.setting(jobname + "_interval")}
			cfg["day"] = self.WEEKDAYS[cfg["day"]] if cfg["day"] >= 0 else -1
			# Adapt job script
			if jobname == "sysupdate":
				cfg["script"] = "RunScript(%s, %s, %s, %s)" %(commons.AddonId(), jobname, commons.getAddonSetting(jobname + "_osupgrade"), commons.getAddonSetting(jobname + "_osintegrity"))
				cfg["type"] = "script"
			elif jobname == "libupdate":
				cfg["script"] = "RunScript(%s, %s, %s, %s)" %(commons.AddonId(), jobname, commons.getAddonSetting(jobname + "_music"), commons.getAddonSetting(jobname + "_video"))
				cfg["type"] = "script"
			elif jobname == "libclean":
				cfg["script"] = "RunScript(%s, %s, %s, %s)" %(commons.AddonId(), jobname, commons.getAddonSetting(jobname + "_music"), commons.getAddonSetting(jobname + "_video"))
				cfg["type"] = "script"
			elif jobname == "sysbackup":
				cfg["script"] = "RunScript(program.recovery, mode=backup)"
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
					commons.error("Job '%s' is removed because no script has been configured to run" %jobname, 'service')
					self.scheduler.remove(job)
				else:
					commons.error("Error creating job based on configuration: %s" %jobname, 'service')
			else:
				commons.debug("Job '%s' is not enabled" %jobname, 'service')



if __name__ == "__main__":
	ClueService()
