# -*- coding: utf-8 -*-

import os
from resources.scheduler import *
from resources.tasks import ServiceTask, GraphicTask, WindowTask

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
		common.debug("Settings have been updated and will trigger re-loading of scheduler jobs", "settings")
		self.updateSettingsMethod()



class ClueService:
	WEEKDAYS = ['monday', "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
	JOBNAMES = [ "sysupdate", "libupdate", "libclean", "recovery", "custom1", "custom2", "custom3", "custom4", "custom5", "custom6", "custom7", "custom8", "custom9", "custom10"]


	def __init__(self):
		# Start jobs according to the input parameters
		if len(sys.argv) <= 1:
			common.debug('%s v%s has been started as service: %s' %(common.AddonName(), common.AddonVersion(), 'service'))
			# Check if it runs for the first time
			self.isFirstTimeRunning()
			self.initScheduler()
			self.initService()
		else:
			_code = str(sys.argv[1]).strip()
			common.info('%s v%s has been started as task: %s' %(common.AddonName(), common.AddonVersion(), _code), 'service')
			_task = self.getTask(_code)
			if _task is not None:
				common.debug("Starting service task [%s] with the following parameters: %s" %(str(_task), str(sys.argv[2::])), 'service')
				_task.run(*sys.argv[2::])
			else:
				common.warn("No task found with identifier: %s" %_code)
		common.debug('%s v%s has been terminated' %(common.AddonName(), common.AddonVersion()), 'service')


	def getTask(self, code):
		"""Returns the service task having the specified signature """
		task = None
		area = None
		if code is None or code == "":
			return task
		else:
			parts = str(code).split(".")
			if len(parts) > 1:
				area = parts[0]
				code = parts[1]
			if area is None or area == ServiceTask.key:
				common.trace("Looking for [%s] task in [%s] area" %(code,area))
				for cls in ServiceTask.__subclasses__():
					try:
						if cls.key == code and cls.__name__ != "GraphicTask" and cls.__name__ != "WindowTask":
							task = cls()
							if task is not None:
								common.debug("Found service task: %s" %task.code())
								break
					except BaseException as be:
						common.error('Unexpected error while calling [%s] service task: %s' %(str(cls),str(be)), 'service')
			if area is None or area == GraphicTask.key:
				common.trace("Looking for [%s] task in [%s] area" %(code,area))
				for cls in GraphicTask.__subclasses__():
					try:
						if cls.key == code:
							task = cls()
							if task is not None:
								common.debug("Found graphic task: %s" %task.code())
								break
					except BaseException as be:
						common.error('Unexpected error while calling [%s] graphic task: %s' %(str(cls),str(be)), 'service')
			if area is None or area == WindowTask.key:
				common.trace("Looking for [%s] task in [%s] area" % (code, area))
				for cls in WindowTask.__subclasses__():
					try:
						if cls.key == code:
							task = cls(cls.__name__ + ".xml", common.AddonPath())
							if task is not None:
								common.debug("Found window task: %s" % task.code())
								break
					except BaseException as be:
						common.error('Unexpected error while calling [%s] window task: %s' %(str(cls),str(be)), 'service')
			return task


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
		# reset screensaver
		common.setSystemSetting("screensaver.mode", "")
		xbmc.sleep(500)
		# setup locale based on your location
		jsondata = common.urlcall("http://ip-api.com/json/", headers={"User-Agent": common.agent()}, output='json')
		if jsondata is not None:
			if "country" in jsondata:
				common.debug("Applying new value to setting [locale.timezonecountry] to: %s" %jsondata['country'])
				common.setSystemSetting("locale.timezonecountry", jsondata['country'])
		xbmc.sleep(500)
		# setup weather addon to enable it and take a default provider
		common.setAddonSetting("weather.clue", "Enabled", True)
		common.setAddonSetting("weather.clue", "ProviderCode", "yahoo")
		xbmc.sleep(500)
		# open Clue Setup console for configuration and parametrization
		common.runBuiltinCommand("RunScript", "service.clue", "setup")


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


	def initService(self):
		# Force screensaver custom configuration
		mode = common.getSystemSetting("screensaver.mode")
		if mode == '' or mode is None:
			common.setSystemSetting("screensaver.mode", "")


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
				cfg["script"] = "RunScript(%s, %s, %s, %s)" %(common.AddonId(), jobname, common.setting(jobname + "_osupgrade"), common.setting(jobname + "_osintegrity"))
				cfg["type"] = "script"
			elif jobname == "libupdate":
				cfg["script"] = "RunScript(%s, %s, %s, %s)" %(common.AddonId(), jobname, common.setting(jobname + "_music"), common.setting(jobname + "_video"))
				cfg["type"] = "script"
			elif jobname == "libclean":
				cfg["script"] = "RunScript(%s, %s, %s, %s)" %(common.AddonId(), jobname, common.setting(jobname + "_music"), common.setting(jobname + "_video"))
				cfg["type"] = "script"
			elif jobname == "recovery":
				cfg["script"] = "RunScript(%s, %s, %s)" %(common.AddonId(), jobname, "mode=%s" %common.setting(jobname + "_type"))
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