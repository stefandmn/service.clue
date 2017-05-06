# -*- coding: utf-8 -*-

from .BaseItem import BaseItem


class DirectoryItem(BaseItem):

	def __init__(self, name, uri, image=u'', fanart=u''):
		BaseItem.__init__(self, name, uri, image, fanart)

	def setName(self, name):
		self._name = unicode(name)
