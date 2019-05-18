# -*- coding: utf-8 -*-

import sys
import commons
from abstract import ServiceRunner

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc

if hasattr(sys.modules["__main__"], "xbmcgui"):
	xbmcgui = sys.modules["__main__"].xbmcgui
else:
	import xbmcgui




class SkinInfo(ServiceRunner):
	NETWORKS = ('SystemSetup.NetworkRepeater', 'SystemSetup.NetworkRouter', 'SystemSetup.NetworkWireless', 'SystemSetup.NetworkMobile')

	def __init__(self, id=10000):
		self.id = id
		self.win = xbmcgui.Window(self.id)


	def code(self):
		return "skininfo"


	def setProperty(self, property):
		self.win.setProperty(property, "true")


	def resetProperty(self, property):
		self.win.setProperty(property, "")


	def getProperty(self, property):
		return commons.any2bool(xbmc.getInfoLabel("Window(%s).Property(%s)" % (str(self.id), property)))


	@property
	def isNetworkRepeater(self):
		return self.getProperty(self.NETWORKS[0])


	@property
	def isNetworkRouter(self):
		return self.getProperty(self.NETWORKS[1])


	@property
	def isNetworkWireless(self):
		return self.getProperty(self.NETWORKS[2])


	@property
	def isNetworkMobile(self):
		return self.getProperty(self.NETWORKS[3])


	def setNetworkRepeater(self):
		return self.setProperty(self.NETWORKS[0])


	def setNetworkRouter(self):
		return self.setProperty(self.NETWORKS[1])


	def setNetworkWireless(self):
		return self.setProperty(self.NETWORKS[2])


	def setNetworkMobile(self):
		return self.setProperty(self.NETWORKS[3])


	def resetNetworkRepeater(self):
		return self.resetProperty(self.NETWORKS[0])


	def resetNetworkRouter(self):
		return self.resetProperty(self.NETWORKS[1])


	def resetNetworkWireless(self):
		return self.resetProperty(self.NETWORKS[2])


	def resetNetworkMobile(self):
		return self.resetProperty(self.NETWORKS[3])


	def run(self, *arg):
		# Check network mode
		_status, _content = commons.procexec("/opt/clue/bin/setup -g network -m")
		if _status:
			if _content is not None and _content == "repeater":
				self.setNetworkRepeater()
				if self.isNetworkRouter:
					self.resetNetworkRouter()
			elif _content is not None and _content == "router":
				self.setNetworkRouter()
				if self.isNetworkRepeater:
					self.resetNetworkRepeater()
			else:
				if self.isNetworkRepeater:
					self.resetNetworkRepeater()
				if self.isNetworkRouter:
					self.resetNetworkRouter()
		# Check network interface
		_status, _content = commons.procexec("/opt/clue/bin/setup -g network -a")
		if _status:
			if _content is not None and _content.startswith("wlan"):
				self.setNetworkWireless()
				if self.isNetworkMobile:
					self.resetNetworkMobile()
			elif _content is not None and (_content.startswith("ppp") or _content.startswith("wwlan")):
				self.setNetworkMobile()
				if self.isNetworkWireless:
					self.resetNetworkWireless()
			else:
				if self.isNetworkWireless:
					self.resetNetworkWireless()
				if self.isNetworkMobile:
					self.resetNetworkMobile()
