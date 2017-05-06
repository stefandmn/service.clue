# -*- coding: utf-8 -*-

from .DirectoryItem import DirectoryItem


class SearchItem(DirectoryItem):

	def __init__(self, context, alt_name=None, image=None, fanart=None):
		name = alt_name
		if not name:
			name = context.localize(30102, "Search")
		if image is None:
			image = context.createResourcePath('media/search.png')
		DirectoryItem.__init__(self, name, context.createUri(['media/search', 'list']), image=image)
		if fanart:
			self.setFanart(fanart)
		else:
			self.setFanart(context.getFanart())
		pass
