# -*- coding: utf-8 -*-

from .DirectoryItem import DirectoryItem


class SearchHistoryItem(DirectoryItem):

	def __init__(self, context, query, image=None, fanart=None):
		if image is None:
			image = context.createResourcePath('media/search.png')
		DirectoryItem.__init__(self, query, context.createUri(['media/search', 'query'], {'q': query}), image=image)
		if fanart:
			self.setFanart(fanart)
		else:
			self.setFanart(context.getFanart())
		context_menu = [(context.localize(30108, "Remove"), 'RunPlugin(%s)' % context.createUri(['media/search', 'remove'], params={'q': query})),
						(context.localize(30113, "Rename"), 'RunPlugin(%s)' % context.createUri(['media/search', 'rename'], params={'q': query})),
						(context.localize(30120, "Clear"), 'RunPlugin(%s)' % context.createUri(['media/search', 'clear']))]
		self.setContextMenu(context_menu)
