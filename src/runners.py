# -*- coding: utf-8 -*-

import abc
import sys
import lib.Commons as commons

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc


class ServiceRunner(object):
	__metaclass__ = abc.ABCMeta

	def __repr__(self):
		return str(self.__class__) + " (" + str(self.code()) + ")"

	@abc.abstractmethod
	def code(self):
		return None
		pass

	@abc.abstractmethod
	def run(self, *arg):
		pass


class LibraryUpdater(ServiceRunner, xbmc.Monitor):

	def __init__(self):
		xbmc.Monitor.__init__(self)
		self.music = False
		self.video = False

	def code(self):
		return "libupdater"

	def detect(self, arg):
		if arg is not None and len(arg) == 1:
			if str(arg[0]).strip().lower() in ('music', 'audio'):
				self.music = True
			elif str(arg[0]).strip().lower() in ('video', 'movies'):
				self.video = True
			else:
				self.music = commons.any2bool(arg[0])
		if arg is not None and len(arg) >= 2:
			self.music = commons.any2bool(arg[0])
			self.video = commons.any2bool(arg[1])

	def apply(self):
		if self.music:
			self.apply4Music()
		elif self.video:
			self.apply4Video()

	def apply4Music(self):
		if not xbmc.getCondVisibility('Library.IsScanningMusic'):
			xbmc.executebuiltin("UpdateLibrary(music)")
			xbmc.sleep(500)
			commons.info("Update of music library have been successfully triggered", "LibraryUpdater")
		else:
			commons.warn("Music library is currently scanned, so the update procedure will be skipped this time", "LibraryUpdater")
			self.music = False

	def apply4Video(self):
		if not xbmc.getCondVisibility('Library.IsScanningVideo'):
			xbmc.executebuiltin("UpdateLibrary(video)")
			xbmc.sleep(500)
			commons.info("Update of video library have been successfully triggered", "LibraryUpdater")
		else:
			commons.warn("Video library is currently scanned, so the update procedure will be skipped this time", "LibraryUpdater")
			self.video = False

	def onScanFinished(self, library):
		if library == "music":
			commons.info("Update of music library have been successfully finished", "LibraryUpdater")
			self.music = False
		elif library == "video":
			commons.info("Update of video library have been successfully finished", "LibraryUpdater")
			self.video = False
		xbmc.sleep(1000)
		if self.music or self.video:
			self.apply()

	def run(self, *arg):
		self.detect(arg)
		self.apply()
		while self.music or self.video:
			xbmc.sleep(1000)


class LibraryCleaner(ServiceRunner, xbmc.Monitor):

	def __init__(self):
		xbmc.Monitor.__init__(self)
		self.music = False
		self.video = False

	def code(self):
		return "libcleaner"

	def detect(self, arg):
		if arg is not None and len(arg) == 1:
			if str(arg[0]).strip().lower() in ('music', 'audio'):
				self.music = True
			elif str(arg[0]).strip().lower() in ('video', 'movies'):
				self.video = True
			else:
				self.music = commons.any2bool(arg[0])
		if arg is not None and len(arg) >= 2:
			self.music = commons.any2bool(arg[0])
			self.video = commons.any2bool(arg[1])

	def apply(self):
		if self.music:
			self.apply4Music()
		elif self.video:
			self.apply4Video()

	def apply4Music(self):
		if not xbmc.getCondVisibility('Library.IsScanningMusic'):
			xbmc.executebuiltin("CleanLibrary(music)")
			xbmc.sleep(500)
			commons.info("Cleaning of music library have been successfully triggered", "LibraryCleaner")
		else:
			commons.warn("Music library is currently scanned, so the cleaning procedure will be skipped this time", "LibraryCleaner")
			self.music = False

	def apply4Video(self):
		if not xbmc.getCondVisibility('Library.IsScanningVideo'):
			xbmc.executebuiltin("CleanLibrary(video)")
			xbmc.sleep(500)
			commons.info("Cleaning of video library have been successfully triggered", "LibraryCleaner")
		else:
			commons.warn("Video library is currently scanned, so the cleaning procedure will be skipped this time", "LibraryCleaner")
			self.video = False

	def onCleanFinished(self, library):
		if library == "music":
			commons.info("Cleaning of music library have been successfully finished", "LibraryCleaner")
			self.music = False
		elif library == "video":
			commons.info("Cleaning of video library have been successfully finished", "LibraryCleaner")
			self.video = False
		xbmc.sleep(1000)
		if self.music or self.video:
			self.apply()

	def run(self, *arg):
		self.detect(arg)
		self.apply()
		while self.music or self.video:
			xbmc.sleep(1000)


class SystemUpdater(ServiceRunner):

	def __init__(self):
		self.osupgrade = False
		self.integrity = False

	def code(self):
		return "sysupdater"

	def detect(self, arg):
		if arg is not None and len(arg) == 1:
			if str(arg[0]).strip().lower() in ('upgrade', 'osupgrade'):
				self.osupgrade = True
			elif str(arg[0]).strip().lower() in ('integrity', 'osintegrity'):
				self.integrity = True
			else:
				self.osupgrade = commons.any2bool(arg[0])
		if arg is not None and len(arg) >= 2:
			self.osupgrade = commons.any2bool(arg[0])
			self.integrity = commons.any2bool(arg[1])

	def run(self, *arg):
		self.detect(arg)
		(_status,_content) = commons.procexec("/opt/clue/bin/setup -g update")
		if _status and commons.any2int(_content.strip()) == 0:
			commons.NotificationMsg(commons.translate(32010))
			_cmd = "/opt/clue/bin/setup -s update -p"
			_opt = "-a" if self.osupgrade else ""
			(_status,_content) = commons.procexec("%s %s" %(_cmd,_opt))
			# Run system integrity procedure
			if _status and self.integrity:
				_cmd = "/opt/clue/bin/setup -s update -s"
				(_status,_content) = commons.procexec(_cmd)
			if _status:
				commons.NotificationMsg(commons.translate(32011))
			else:
				commons.NotificationMsg(commons.translate(32012))
		else:
			commons.warn("System update is currently running, so the update procedure will be skipped this time", "SystemUpdate")


class GuiUpdater(ServiceRunner):

	def code(self):
		return "guiupdater"

	def run(self, *arg):
		# Check network mode
		_status,_content = commons.procexec("/opt/clue/bin/setup -g network -m")
		if _status:
			if _content is not None and _content == "repeater":
				xbmc.executebuiltin("Skin.SetBool(NetworkRepeater)")
				if xbmc.getCondVisibility("Skin.HasSetting(NetworkRouter)"):
					xbmc.executebuiltin("Skin.ToggleSetting(NetworkRouter)")
			elif _content is not None and _content == "router":
				xbmc.executebuiltin("Skin.SetBool(NetworkRouter)")
				if xbmc.getCondVisibility("Skin.HasSetting(NetworkRepeater)"):
					xbmc.executebuiltin("Skin.ToggleSetting(NetworkRepeater)")
			else:
				if xbmc.getCondVisibility("Skin.HasSetting(NetworkRepeater)"):
					xbmc.executebuiltin("Skin.ToggleSetting(NetworkRepeater)")
				if xbmc.getCondVisibility("Skin.HasSetting(NetworkRouter)"):
					xbmc.executebuiltin("Skin.ToggleSetting(NetworkRouter)")
		# Check network interface
		_status,_content = commons.procexec("/opt/clue/bin/setup -g network -a")
		if _status:
			if _content is not None and _content.startswith("wlan"):
				xbmc.executebuiltin("Skin.SetBool(NetworkWireless)")
				if xbmc.getCondVisibility("Skin.HasSetting(NetworkMobile)"):
					xbmc.executebuiltin("Skin.ToggleSetting(NetworkMobile)")
			elif _content is not None and (_content.startswith("ppp") or _content.startswith("wwlan")):
				xbmc.executebuiltin("Skin.SetBool(NetworkMobile)")
				if xbmc.getCondVisibility("Skin.HasSetting(NetworkWireless)"):
					xbmc.executebuiltin("Skin.ToggleSetting(NetworkWireless)")
			else:
				if xbmc.getCondVisibility("Skin.HasSetting(NetworkWireless)"):
					xbmc.executebuiltin("Skin.ToggleSetting(NetworkWireless)")
				if xbmc.getCondVisibility("Skin.HasSetting(NetworkMobile)"):
					xbmc.executebuiltin("Skin.ToggleSetting(NetworkMobile)")


class CecTrigger(ServiceRunner):

	def code(self):
		return "cectrigger"

	def run(self, *arg):
		action = arg[0] if len(arg) > 0 else None
		if action is None or action == 'toggle':
			xbmc.executebuiltin("CECToggleState")
		elif action == 'start' or action == 'active':
			xbmc.executebuiltin("CECActivateSource")
		elif action == 'standby':
			xbmc.executebuiltin("CECStandby")
