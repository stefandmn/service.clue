#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import xbmc
import xbmcaddon

from lib.Scheduler import SchedulerManager
import lib.Commons as common

packages 		= ['clue-mcpi', 'clue-mcrep']
platforms		= ['clue', 'debian', 'ubuntu']


class ClueService:

	def __init__(self):
		common.info('%s version %s has been started' %(xbmcaddon.Addon().getAddonInfo('name'), xbmcaddon.Addon().getAddonInfo('version')))
		# Check if it runs for the first time
		self.isFirstTime()
		# Start jobs according to the input parameters
		if not sys.argv[0] or sys.argv[0] and sys.argv[1] == 'scheduler':
			self.scheduler()
		elif sys.argv[0] and sys.argv[1] == 'systemupdate':
			runSystemUpdate()
		elif sys.argv[0] and sys.argv[1] == 'musiclibupdate':
			runMusicLibUpdate()
		elif sys.argv[0] and sys.argv[1] == 'videolibupdate':
			runVideoLibUpdate()
		common.debug('%s version %s has been terminated' %(xbmcaddon.Addon().getAddonInfo('name'), xbmcaddon.Addon().getAddonInfo('version')))

	def isFirstTime(self):
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

	def scheduler(self):
		scron = SchedulerManager()
		scron.start()

def runMusicLibUpdate():
	if xbmcaddon.Addon().getSetting("musiclib") == "true":
		if not xbmc.getCondVisibility('Library.IsScanningMusic'):
			if xbmcaddon.Addon().getSetting("musiclib_clean") == "true":
				xbmc.executebuiltin("CleanLibrary(music)")
			xbmc.executebuiltin("UpdateLibrary(music)")
			common.info("Update of music library have been executed successfully", "MusicLibUpdate")
		else:
			common.warn("Music library are currently scanned, so the update procedure will be skipped this time", "MusicLibUpdate")


def runVideoLibUpdate():
	if xbmcaddon.Addon().getSetting("videolib") == "true":
		if not xbmc.getCondVisibility('Library.IsScanningVideo'):
			if xbmcaddon.Addon().getSetting("videolib_clean") == "true":
				xbmc.executebuiltin("CleanLibrary(video)")
			xbmc.executebuiltin("UpdateLibrary(video)")
			common.info("Update of video library have been executed successfully", "VideoLibUpdate")
		else:
			common.warn("Video library are currently scanned, so the update procedure will be skipped this time", "VideoLibUpdate")


def runSystemUpdate():
	print


if (__name__ == "__main__"):
	ClueService()