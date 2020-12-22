# -*- coding: utf-8 -*-

import os
import sys
import json
import common
from .abcservice import ServiceTask

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc



class Favourites(ServiceTask):
	key = "favourites"


	def code(self):
		return self.key


	def run(self, *args):
		params = {}
		if len(args) > 1:
			for i in args:
				arg = i
				if arg.startswith('?'):
					arg = arg[1:]
				params.update(dict(common.urlparsequery(arg)))
		if not "type" in params:
			params['type'] = "media"
		if not "path" in params:
			if xbmc.Player().isPlayingAudio():
				params['path'] = xbmc.Player().getPlayingFile()
				if not "title" in params:
					params['title'] = xbmc.Player().getMusicInfoTag().getArtist().strip() + " - " + xbmc.Player().getMusicInfoTag().getTitle().strip()
			elif xbmc.Player().isPlayingVideo():
				params['path'] = xbmc.Player().getPlayingFile()
				if not "title" in params:
					params['title'] = xbmc.Player().getVideoInfoTag().getTitle().strip()
		if not "title" in params:
			params['title'] = os.path.basename(params['path'])
		if "path" in params:
			self.add(params)
		else:
			common.error("No reference specified for the new item in Favourites container!", "service.Runner.Favourites")


	def add(self, params):
		cmd = {"jsonrpc": "2.0", "method": "Favourites.AddFavourite", "params": {"title": params["title"], "type": params["type"], "path": params["path"]}, "id": "1"}
		answer = json.loads(xbmc.executeJSONRPC(json.dumps(cmd)))
		common.info("Adding favourite item: %s" % answer, "Favourites")
