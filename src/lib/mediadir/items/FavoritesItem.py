# -*- coding: utf-8 -*-

from .DirectoryItem import DirectoryItem


class FavoritesItem(DirectoryItem):

	def __init__(self, context, alt_name=None, image=None, fanart=None):
		name = alt_name
		if not name:
			name = context.localize(30100, "Favorites")
		if image is None:
			image = context.createResourcePath('media/favorites.png')
		DirectoryItem.__init__(self, name, context.createUri(['media/favorites', 'list']), image=image)
		if fanart:
			self.setFanart(fanart)
		else:
			self.setFanart(context.getFanart())
		pass
