# -*- coding: utf-8 -*-

import xbmcgui
import xbmcplugin
from mediadir.AbstractRunner import AbstractRunner
from mediadir.FrameworkException import FrameworkException
from mediadir.items.DirectoryItem import DirectoryItem
from mediadir.items.VideoItem import VideoItem
from mediadir.items.AudioItem import AudioItem
from mediadir.items.ImageItem import ImageItem
from mediadir.items.UriItem import UriItem
from mediadir import AbstractProvider
from mediadir.utils import MediaItems, InfoLabels


class ClueRunner(AbstractRunner):

	def __init__(self):
		AbstractRunner.__init__(self)

	def run(self, provider, context=None):
		try:
			options = {}
			results = provider.navigate(context)
			result = results[0]
			options.update(results[1])
			if isinstance(result, bool) and not result:
				xbmcplugin.endOfDirectory(context.getHandle(), succeeded=False)
			elif isinstance(result, VideoItem) or isinstance(result, AudioItem) or isinstance(result, UriItem):
				self._set_resolved_url(context, result)
			elif isinstance(result, DirectoryItem):
				self._add_directory(context, result)
			elif isinstance(result, list):
				item_count = len(result)
				for item in result:
					if isinstance(item, DirectoryItem):
						self._add_directory(context, item, item_count)
					elif isinstance(item, VideoItem):
						self._add_video(context, item, item_count)
					elif isinstance(item, AudioItem):
						self._add_audio(context, item, item_count)
					elif isinstance(item, ImageItem):
						self._add_image(context, item, item_count)
				xbmcplugin.endOfDirectory(context.getHandle(), succeeded=True, cacheToDisc=options.get(AbstractProvider.RESULT_CACHE_TO_DISC, True))
		except FrameworkException, ex:
			if provider.handleException(context, ex):
				context.error(ex.__str__())
				xbmcgui.Dialog().ok("Exception in ContentProvider", ex.__str__())

	def _set_resolved_url(self, context, base_item, succeeded=True):
		item = MediaItems.to_item(context, base_item)
		item.setPath(base_item.getUri())
		xbmcplugin.setResolvedUrl(context.getHandle(), succeeded=succeeded, listitem=item)

	def _add_directory(self, context, directory_item, item_count=0):
		item = xbmcgui.ListItem(label=directory_item.getName(), iconImage=u'DefaultFolder.png', thumbnailImage=directory_item.getImage())
		# only set fanart is enabled
		settings = context.getSettings()
		if directory_item.getFanart() and settings.showFanart():
			item.setProperty(u'fanart_image', directory_item.getFanart())
		if directory_item.getContextMenu() is not None:
			item.addContextMenuItems(directory_item.getContextMenu(), replaceItems=directory_item.getReplaceContextMenu())
		xbmcplugin.addDirectoryItem(handle=context.getHandle(), url=directory_item.getUri(), listitem=item, isFolder=True, totalItems=item_count)

	def _add_video(self, context, video_item, item_count=0):
		item = MediaItems.to_video_item(context, video_item)
		xbmcplugin.addDirectoryItem(handle=context.getHandle(), url=video_item.getUri(), listitem=item, totalItems=item_count)

	def _add_image(self, context, image_item, item_count):
		item = xbmcgui.ListItem(label=image_item.getName(), iconImage=u'DefaultPicture.png', thumbnailImage=image_item.getImage())
		# only set fanart is enabled
		settings = context.getSettings()
		if image_item.getFanart() and settings.showFanart():
			item.setProperty(u'fanart_image', image_item.getFanart())
		if image_item.getContextMenu() is not None:
			item.addContextMenuItems(image_item.getContextMenu(), replaceItems=image_item.getReplaceContextMenu())
		item.setInfo(type=u'picture', infoLabels=InfoLabels.createFromItem(context, image_item))
		xbmcplugin.addDirectoryItem(handle=context.getHandle(), url=image_item.getUri(), listitem=item, totalItems=item_count)

	def _add_audio(self, context, audio_item, item_count):
		item = MediaItems.to_audio_item(context, audio_item)
		xbmcplugin.addDirectoryItem(handle=context.getHandle(), url=audio_item.getUri(), listitem=item, totalItems=item_count)
