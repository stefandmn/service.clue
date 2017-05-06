# -*- coding: utf-8 -*-

from .DirectoryItem import DirectoryItem


class NextPageItem(DirectoryItem):

	def __init__(self, context, current_page=1, image=None, fanart=None):
		new_params = {}
		new_params.update(context.getParams())
		new_params['page'] = unicode(current_page + 1)
		name = context.localize(30106, 'Next Page')
		if name.find('%d') != -1:
			name %= current_page + 1
		DirectoryItem.__init__(self, name, context.createUri(context.getPath(), new_params), image=image)
		if fanart:
			self.setFanart(fanart)
		else:
			self.setFanart(context.getFanart())
		pass
