# -*- coding: utf-8 -*-

import sys
import common
from .abcservice import ServiceTask

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc



class LibraryUpdater(ServiceTask, xbmc.Monitor):
	ley = "libupdate"


	def __init__(self):
		ServiceTask.__init__(self)
		xbmc.Monitor.__init__(self)
		self.music = False
		self.video = False


	def detect(self, args):
		if args is not None and len(args) == 1:
			if str(args[0]).strip().lower() in ('music', 'audio'):
				self.music = True
			elif str(args[0]).strip().lower() in ('video', 'movies'):
				self.video = True
			else:
				self.music = common.any2bool(args[0])
		if args is not None and len(args) >= 2:
			self.music = common.any2bool(args[0])
			self.video = common.any2bool(args[1])


	def apply(self):
		if self.music:
			self.apply4Music()
		elif self.video:
			self.apply4Video()


	def apply4Music(self):
		if not xbmc.getCondVisibility('Library.IsScanningMusic'):
			xbmc.executebuiltin("UpdateLibrary(music)")
			xbmc.sleep(500)
			self.info("Update of music library have been successfully triggered")
		else:
			self.warn("Music library is currently scanned, so the update procedure will be skipped this time")
			self.music = False


	def apply4Video(self):
		if not xbmc.getCondVisibility('Library.IsScanningVideo'):
			xbmc.executebuiltin("UpdateLibrary(video)")
			xbmc.sleep(500)
			self.info("Update of video library have been successfully triggered")
		else:
			self.warn("Video library is currently scanned, so the update procedure will be skipped this time")
			self.video = False


	def onScanFinished(self, library):
		if library == "music":
			self.info("Update of music library have been successfully finished")
			self.music = False
		elif library == "video":
			self.info("Update of video library have been successfully finished")
			self.video = False
		xbmc.sleep(1000)
		if self.music or self.video:
			self.apply()


	def run(self, *arg):
		self.detect(arg)
		self.apply()
		while self.music or self.video:
			xbmc.sleep(1000)
