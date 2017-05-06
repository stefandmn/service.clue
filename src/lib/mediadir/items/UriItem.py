# -*- coding: utf-8 -*-

from .BaseItem import BaseItem


class UriItem(BaseItem):

	def __init__(self, uri):
		BaseItem.__init__(self, name=u'', uri=uri)
