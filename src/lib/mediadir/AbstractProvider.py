# -*- coding: utf-8 -*-

import re
import utils.ItemCast as items
from .FrameworkException import FrameworkException
from items.SearchHistoryItem import SearchHistoryItem
from items.NewSearchItem import NewSearchItem


class AbstractProvider(object):

	RESULT_CACHE_TO_DISC = 'cache_to_disc'  # (bool)

	def __init__(self):
		self._local_map = {
			'wizard.view.default': 30027,
			'wizard.view.episodes': 30028,
			'wizard.view.movies': 30029,
			'wizard.view.tvshows': 30032,
			'wizard.view.songs': 30033,
			'wizard.view.artists': 30034,
			'wizard.view.albums': 30035 }
		# map for regular expression (path) to method (names)
		self._dict_path = {}
		# register some default paths
		self.register_path('^/$', '_internal_root')
		self.register_path('^/media/watch_later/(?P<command>add|remove|list)/?$', '_internal_watch_later')
		self.register_path('^/media/favorites/(?P<command>add|remove|list)/?$', '_internal_favorite')
		self.register_path('^/media/search/(?P<command>input|query|list|remove|clear|rename)/?$', '_internal_search')
		self.register_path('(?P<path>.*\/)extrafanart\/([\?#].+)?$', '_internal_on_extra_fanart')
		for method_name in dir(self):
			method = getattr(self, method_name)
			if hasattr(method, 'media_re_path'):
				self.register_path(method.media_re_path, method_name)
		pass

	def getAlternativeFanart(self, context):
		return context.getFanart()

	def register_path(self, re_path, method_name):
		"""
		Registers a new method by name (string) for the given regular expression
		:param re_path: regular expression of the path
		:param method_name: name of the method
		:return:
		"""
		self._dict_path[re_path] = method_name

	def navigate(self, context):
		path = context.getPath()
		for key in self._dict_path:
			re_match = re.search(key, path, re.UNICODE)
			if re_match is not None:
				method_name = self._dict_path.get(key, '')
				method = getattr(self, method_name)
				if method is not None:
					if hasattr(method, 'media_re_path'):
						context.debug("Preparing to run registered path: %s" %method.media_re_path)
					else:
						context.debug("Preparing to run method: %s" %method.__name__ )
					result = method(context, re_match)
					if not isinstance(result, tuple):
						result = result, {}
					return result
		raise FrameworkException("Mapping for path '%s' not found" % path)

	def on_extra_fanart(self, context, re_match):
		# The implementation of the provider can override this behavior.
		return None

	def _internal_on_extra_fanart(self, context, re_match):
		path = re_match.group('path')
		new_context = context.clone(new_path=path)
		return self.on_extra_fanart(new_context, re_match)

	def onSearch(self, search_text, context, re_match):
		raise NotImplementedError()

	def onRoot(self, context, re_match):
		raise NotImplementedError()

	def onWatchLater(self, context, re_match):
		pass

	def _internal_root(self, context, re_match):
		context.getUI().showBusyDialog()
		try:
			result = self.onRoot(context, re_match)
		except BaseException as error:
			result = error
		context.getUI().closeBusyDialog()
		if isinstance(result, BaseException):
			raise result
		else:
			return result

	def _internal_favorite(self, context, re_match):
		#context.addSortMethod('SORT_METHOD_LABEL_IGNORE_THE')
		params = context.getParams()
		command = re_match.group('command')
		if command == 'add':
			fav_item = items.from_json(params['item'])
			context.getFavoriteList().add(fav_item)
		elif command == 'remove':
			fav_item = items.from_json(params['item'])
			context.getFavoriteList().remove(fav_item)
			context.getUI().refreshContainer()
		elif command == 'list':
			directory_items = context.getFavoriteList().list()
			for directory_item in directory_items:
				context_menu = [(context.localize(30108, "Remove"), 'RunPlugin(%s)' % context.createUri(['media/favorites', 'remove'], params={'item': items.to_jsons(directory_item)}))]
				directory_item.setContextMenu(context_menu)
			return directory_items
		else:
			pass
		pass

	def _internal_watch_later(self, context, re_match):
		self.onWatchLater(context, re_match)
		params = context.getParams()
		command = re_match.group('command')
		if command == 'add':
			item = items.from_json(params['item'])
			context.getWatchLaterList().add(item)
		elif command == 'remove':
			item = items.from_json(params['item'])
			context.getWatchLaterList().remove(item)
			context.getUI().refreshContainer()
		elif command == 'list':
			video_items = context.getWatchLaterList().list()
			for video_item in video_items:
				context_menu = [(context.localize(30108, "Remove"), 'RunPlugin(%s)' % context.createUri(['media/watch_later', 'remove'], params={'item': items.to_jsons(video_item)}))]
				video_item.setContextMenu(context_menu)
			return video_items
		else:
			# do something
			pass
		pass

	def _internal_search(self, context, re_match):
		params = context.getParams()
		command = re_match.group('command')
		search_history = context.getSearchHistory()
		if command == 'remove':
			context.getUI().showBusyDialog()
			try:
				query = params['q']
				search_history.remove(query)
				context.getUI().refreshContainer()
				result = True
			except BaseException as error:
				result = error
			context.getUI().closeBusyDialog()
			if isinstance(result, BaseException):
				raise result
			else:
				return result
		elif command == 'rename':
			query = params['q']
			result, new_query = context.getUI().onKeyboardInput(context.localize(30113, "Rename"), query)
			if result:
				context.getUI().showBusyDialog()
				try:
					search_history.rename(query, new_query)
					context.getUI().refreshContainer()
					result = True
				except BaseException as error:
					result = error
				context.getUI().closeBusyDialog()
				if isinstance(result, BaseException):
					raise result
				else:
					return result
			else:
				return True
		elif command == 'clear':
			context.getUI().showBusyDialog()
			try:
				search_history.clear()
				context.getUI().refreshContainer()
				result = True
			except BaseException as error:
				result = error
			context.getUI().closeBusyDialog()
			if isinstance(result, BaseException):
				raise result
			else:
				return result
		elif command == 'input':
			result, query = context.getUI().onKeyboardInput(context.localize(30102, "Search"))
			if result:
				context.execute('Container.Update(%s)' % context.createUri(['media/search', 'query'], {'q': query}))
				pass
			return True
		elif command == 'query':
			context.getUI().showBusyDialog()
			try:
				query = params['q']
				search_history.update(query)
				result = self.onSearch(query, context, re_match)
			except BaseException as error:
				result = error
			context.getUI().closeBusyDialog()
			if isinstance(result, BaseException):
				raise result
			else:
				return result
		else:
			result = []
			# 'New Search...'
			new_search_item = NewSearchItem(context, fanart=self.getAlternativeFanart(context))
			result.append(new_search_item)
			for search in search_history.list():
				# little fallback for old history entries
				if isinstance(search, items.DirectoryItem):
					search = search.getName()
					pass
				# we create a new instance of the SearchItem
				search_history_item = SearchHistoryItem(context, search, fanart=self.getAlternativeFanart(context))
				result.append(search_history_item)
				pass
			if search_history.is_empty():
				pass
			return result, {self.RESULT_CACHE_TO_DISC: False}

	def handleException(self, context, exception_to_handle):
		return True
