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
		common.debug("Settings have been updated and will trigger re-loading of scheduler jobs", "service.Settings")
		self.updateSettingsMethod()



class ClueService:
	WEEKDAYS = ['monday', "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
	JOBNAMES = [ "sysupdate", "libupdate", "libclean", "sysbackup", "custom1", "custom2", "custom3", "custom4", "custom5", "custom6", "custom7", "custom8", "custom9", "custom10"]
	RUNNERS = {}


	def __init__(self):
		# Start jobs according to the input parameters
		if len(sys.argv) <= 1:
			common.debug('%s v%s has been started: %s' %(common.AddonName(), common.AddonVersion(), 'service'))
			# Check if it runs for the first time
			self.isFirstTimeRunning()
			self.initScheduler()
		else:
			_code = str(sys.argv[1]).strip()
			common.info('%s v%s has been started: %s' %(common.AddonName(), common.AddonVersion(), _code), 'service')
			_runner = self.getRunner(_code)
			if _runner is not None:
				common.debug("Starting service runner: %s" %str(_runner), 'service')
				_runner.run(*sys.argv[2::])
			else:
				common.error("Unknown service runner: %s" %_code)
		common.debug('%s v%s has been terminated' %(common.AddonName(), common.AddonVersion()), 'service')


	def readRunners(self):
		"""Detect all implemented and declared service runners and build up the corresponding dictionary"""
		self.RUNNERS.clear()
		for cls in ServiceRunner.__subclasses__():
			try:
				runner = cls()
				if not self.RUNNERS.has_key(runner.code()):
					self.RUNNERS[runner.code()] = runner
				else:
					common.error("Invalid signature of service runner, it has the same id with another one: %s " %runner, 'service')
			except BaseException as be:
				common.error('Unexpected error while reading [%s] service runner: %s' %(str(cls),str(be)), 'service')


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
		addondata = xbmc.translatePath("special://profile/addon_data/%s/" %common.AddonId())
		firstlock = os.path.join(addondata, '.firstrun')
		if not os.path.isfile(firstlock):
			if not os.path.exists(addondata):
				os.mkdir(addondata)
			open(firstlock, 'w').close()
			firstrun = threading.Thread(target=self._runFirstTime)
			firstrun.start()


	def _runFirstTime(self):
		xbmc.sleep(5000)
		common.notice("Running for the first time and start Clue System Setup add-on to review and update default system configuration", 'service')
		xbmc.executebuiltin('XBMC.RunScript(program.clue)')


	def initScheduler(self):
		infoFlag = common.any2bool(xbmc.getInfoLabel("Window(10000).Property(SystemSetup.SchedulerStatus)"))
		if not infoFlag:
			xbmcgui.Window(10000).setProperty("SystemSetup.SchedulerStatus", "true")
			self.settings = ServiceSettings(updateSettingsMethod=self.setupScheduler)
			self.scheduler = Scheduler()
			self.setupScheduler()
			self.startScheduler()
		else:
			common.notice("Service component is already running!", 'service')


	def setupScheduler(self):
		self.scheduler.removeAll()
		self.loadScheduler()


	def startScheduler(self):
		while not xbmc.abortRequested:
			self.scheduler.run()
			xbmc.sleep(1000)


	def loadScheduler(self):
		common.debug("Loading scheduler settings..", 'service')
		for jobname in self.JOBNAMES:
			job = None
			cfg = {
					"enabled": common.setting(jobname),
					"cycle": common.setting(jobname + "_cycle"),		# cycles: Weekly(0), Daily(1), Hourly(2), Minutes(3)
					"script": common.setting(jobname + "_script"),
					"type": common.setting(jobname + "_type"),			# script, addon, plugin, command, process, json
					"day": common.setting(jobname + "_day"),
					"time": common.setting(jobname + "_time"),
					"interval": common.setting(jobname + "_interval")}
			cfg["day"] = self.WEEKDAYS[cfg["day"]] if cfg["day"] >= 0 else -1
			# Adapt job script
			if jobname == "sysupdate":
				cfg["script"] = "RunScript(%s, %s, %s, %s)" %(common.AddonId(), jobname, common.getAddonSetting(jobname + "_osupgrade"), common.getAddonSetting(jobname + "_osintegrity"))
				cfg["type"] = "script"
			elif jobname == "libupdate":
				cfg["script"] = "RunScript(%s, %s, %s, %s)" %(common.AddonId(), jobname, common.getAddonSetting(jobname + "_music"), common.getAddonSetting(jobname + "_video"))
				cfg["type"] = "script"
			elif jobname == "libclean":
				cfg["script"] = "RunScript(%s, %s, %s, %s)" %(common.AddonId(), jobname, common.getAddonSetting(jobname + "_music"), common.getAddonSetting(jobname + "_video"))
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
					common.debug("Creating job: %s" %str(job))
				elif job is not None and not cfg["script"]:
					common.error("Job '%s' is removed because no script has been configured to run" %jobname, 'service')
					self.scheduler.remove(job)
				else:
					common.error("Error creating job based on configuration: %s" %jobname, 'service')
			else:
				common.debug("Job '%s' is not enabled" %jobname, 'service')



if __name__ == "__main__":
	ClueService()
