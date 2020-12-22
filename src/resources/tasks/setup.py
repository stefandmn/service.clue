# -*- coding: utf-8 -*-

from .abcwindow import WindowTask


class ClueSetup(WindowTask):
	key = "setup"

	def code(self):
		return self.key
