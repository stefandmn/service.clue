#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import platform
import lib.CommonFunctions as common
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs


packages 		= ['clue-mcpi', 'clue-mcrep']
platforms		= ['clue', 'debian', 'ubuntu']


class Main:

	def __init__(self):
		# Check if it runs for the first time
		runFirstTime()
		# Start jobs according to the input parameters
		if not sys.argv[0]:
			# set to run after boot cache server and system scheduler
			xbmc.executebuiltin('AlarmClock(Scheduler,RunScript(service.clue,scheduler),00:00:10,silent)')
			xbmc.executebuiltin('AlarmClock(StorageServer,RunScript(service.clue,storageserver),00:00:20,silent)')
		elif sys.argv[0] and sys.argv[1] == 'scheduler':
			runScheduler()
		elif sys.argv[0] and sys.argv[1] == 'storageserver':
			runCacheServer()
		elif sys.argv[0] and sys.argv[1] == 'systemupdate':
			runSystemUpdate()
		elif sys.argv[0] and sys.argv[1] == 'musiclibupdate':
			runMusicLibUpdate()
		elif sys.argv[0] and sys.argv[1] == 'videolibupdate':
			runVideoLibUpdate()

def runFirstTime():
	# check if first run
	addondata = xbmc.translatePath("special://profile/addon_data/%s/" %xbmcaddon.Addon().getAddonInfo('id'))
	firstlock = os.path.join(addondata, '.firstrun')
	if not os.path.isfile(firstlock):
		if not os.path.exists(addondata):
			os.mkdir(addondata)
		# Run plugin for configuration
		common.notice("Run for the firt time and start Clue Plugin to review and update default system configuration")
		xbmc.executebuiltin('XBMC.RunScript(plugin.clue)')
		open(firstlock, 'w').close()

def runSystemUpdate():
	if xbmcaddon.Addon().getSetting("system") == "true":
		if xbmc.getCondVisibility('System.Platform.Linux') and platform.dist()[0].lower() in platforms:
			try:
				# try aptdeamon first
				from lib.AptDaemonHandler import AptDaemonHandler
				handler = AptDaemonHandler()
				common.debug("Running AptDaemon handler..", "SystemUpdate")
			except:
				# fallback to shell - since we need the user password, ask to check for new version first
				from lib.AptShellHandler import AptShellHandler
				handler = AptShellHandler(False)
				common.debug("Running AptShell handler..", "SystemUpdate")

			if handler:
				found = False
				for package in packages:
					found = handler.CheckUpgradeAvailable(package)
					if found:
						break
				if found:
					if common.YesNoDialog(32011):
						result = False
						for package in packages:
							if handler.CheckUpgradeAvailable(package):
								result |= handler.UpgradePackage(package)
						if result:
							common.NotificationMsg(32012)
						# check if entire system update is allowed
						if xbmcaddon.Addon().getSetting("system_osupgrade") == "true":
							result = handler.UpgradeSystem()
							if result:
								common.NotificationMsg(32013)
								common.AskRestart(32015, 1)
						else:
							common.AskRestart(32014)
					else:
						if common.YesNoDialog(32010):
							common.info("Disabling add-on by user request")
							xbmcaddon.Addon().setSetting("system", 'false')
			else:
				common.error("No system update handler found", "SystemUpdate")
		else:
			common.error("Unsupported platform %s" %platform.dist()[0], "SystemUpdate")


def runMusicLibUpdate():
	if xbmcaddon.Addon().getSetting("musiclib") == "true":
		if not xbmc.getCondVisibility('Library.IsScanningMusic'):
			xbmc.executebuiltin("UpdateLibrary(music)")
			common.info("Update of music library have been executed successfully", "MusicLibUpdate")
		else:
			common.warn("Music library are currently scanned, so the update procedure will be skipped this time", "MusicLibUpdate")


def runVideoLibUpdate():
	if xbmcaddon.Addon().getSetting("videolib") == "true":
		if not xbmc.getCondVisibility('Library.IsScanningVideo'):
			xbmc.executebuiltin("UpdateLibrary(video)")
			common.info("Update of video library have been executed successfully", "VideoLibUpdate")
		else:
			common.warn("Video library are currently scanned, so the update procedure will be skipped this time", "VideoLibUpdate")


def runCacheServer():
	if xbmcaddon.Addon().getSetting("cacheserver_autostart") == "true":
		sys.path = [xbmcaddon.Addon().getAddonInfo('path') + "/lib"] + sys.path
		common.debug("System path has been updated: %s" %sys.path, "StorageServer")
		import lib.StorageServer as StorageServer
		s = StorageServer.StorageServer(False)
		s.run()
		return True
	else:
		return False


def runScheduler():
	from lib.Scheduler import SchedulerManager
	scron = SchedulerManager()
	scron.start()


if (__name__ == "__main__"):
	common.info('%s version %s has been started' %(xbmcaddon.Addon().getAddonInfo('name'), xbmcaddon.Addon().getAddonInfo('version') ))
	Main()
	common.debug('%s version %s has been terminated' %(xbmcaddon.Addon().getAddonInfo('name'), xbmcaddon.Addon().getAddonInfo('version') ))