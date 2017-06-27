# -*- coding: utf-8 -*-

import sys
import lib.Commons as commons
from service import ClueServiceRunner

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc


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


class ClueSkinUpdate(ClueServiceRunner):

	def code(self):
		return "skinupdate"

	def run(self):
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


class ClueCecActive(ClueServiceRunner):

	def code(self):
		return "cecactive"

	def run(self):
		xbmc.executebuiltin("CECActivateSource")


class ClueCecStandby(ClueServiceRunner):

	def code(self):
		return "cecstandby"

	def run(self):
		xbmc.executebuiltin("CECStandby")


class ClueCecToggle(ClueServiceRunner):

	def code(self):
		return "cectoggle"

	def run(self):
		xbmc.executebuiltin("CECToggleState")
