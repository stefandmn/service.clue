# -*- coding: utf-8 -*-

import sys
import common
from .abcservice import ServiceTask

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc



class LibraryCleaner(ServiceTask, xbmc.Monitor):
	key = "libclean"


	def __init__(self):
		xbmc.Monitor.__init__(self)
		ServiceTask.__init__(self)
		self.music = False
		self.video = False


	def detect(self, arg):
		if arg is not None and len(arg) == 1:
			if str(arg[0]).strip().lower() in ('music', 'audio'):
				self.music = True
			elif str(arg[0]).strip().lower() in ('video', 'movies'):
				self.video = True
			else:
				self.music = common.any2bool(arg[0])
		if arg is not None and len(arg) >= 2:
			self.music = common.any2bool(arg[0])
			self.video = common.any2bool(arg[1])


	def apply(self):
		if self.music:
			self.apply4Music()
		elif self.video:
			self.apply4Video()


	def apply4Music(self):
		if not xbmc.getCondVisibility('Library.IsScanningMusic'):
			xbmc.executebuiltin("CleanLibrary(music)")
			xbmc.sleep(500)
			self.info("Cleaning of music library have been successfully triggered")
		else:
			self.warn("Music library is currently scanned, so the cleaning procedure will be skipped this time")
			self.music = False


	def apply4Video(self):
		if not xbmc.getCondVisibility('Library.IsScanningVideo'):
			xbmc.executebuiltin("CleanLibrary(video)")
			xbmc.sleep(500)
			self.info("Cleaning of video library have been successfully triggered")
		else:
			self.warn("Video library is currently scanned, so the cleaning procedure will be skipped this time")
			self.video = False


	def onCleanFinished(self, library):
		if library == "music":
			self.info("Cleaning of music library have been successfully finished")
			self.music = False
		elif library == "video":
			self.info("Cleaning of video library have been successfully finished")
			self.video = False
		xbmc.sleep(1000)
		if self.music or self.video:
			self.apply()


	def run(self, *arg):
		self.detect(arg)
		self.apply()
		while self.music or self.video:
			xbmc.sleep(1000)
