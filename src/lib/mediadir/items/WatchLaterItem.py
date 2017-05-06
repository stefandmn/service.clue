# -*- coding: utf-8 -*-

from .DirectoryItem import DirectoryItem


class WatchLaterItem(DirectoryItem):

	def __init__(self, context, alt_name=None, image=None, fanart=None):
		name = alt_name
		if not name:
			name = context.localize(30107, "Watch Later")
		if image is None:
			image = context.createResourcePath('media/watch_later.png')
		DirectoryItem.__init__(self, name, context.createUri(['media/watch_later', 'list']), image=image)
		if fanart:
			self.setFanart(fanart)
		else:
			self.setFanart(context.getFanart())
		pass
