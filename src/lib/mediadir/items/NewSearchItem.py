# -*- coding: utf-8 -*-

from .DirectoryItem import DirectoryItem


class NewSearchItem(DirectoryItem):

	def __init__(self, context, alt_name=None, image=None, fanart=None):
		name = alt_name
		if not name:
			name = '[B]' + context.localize(30110, "New Search") + '[/B]'
		if image is None:
			image = context.createResourcePath('media/new_search.png')
		DirectoryItem.__init__(self, name, context.createUri(['media/search', 'input']), image=image)
		if fanart:
			self.setFanart(fanart)
		else:
			self.setFanart(context.getFanart())
		pass

