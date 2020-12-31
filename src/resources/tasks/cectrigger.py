# -*- coding: utf-8 -*-

import sys
from .abcservice import ServiceTask

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc



class CecTrigger(ServiceTask):
	key = "cectrigger"


	def run(self, *arg):
		action = arg[0] if len(arg) > 0 else None
		if action is None or action == 'toggle':
			xbmc.executebuiltin("CECToggleState")
		elif action == 'start' or action == 'active':
			xbmc.executebuiltin("CECActivateSource")
		elif action == 'standby':
			xbmc.executebuiltin("CECStandby")
