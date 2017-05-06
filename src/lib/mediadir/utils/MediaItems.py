# -*- coding: utf-8 -*-

import xbmcgui
from mediadir.utils import InfoLabels
from mediadir.items.VideoItem import VideoItem
from mediadir.items.AudioItem import AudioItem
from mediadir.items.UriItem import UriItem


def to_video_item(context, video_item):
	context.debug('Converting VideoItem')
	major_version = context.getSystemVersion().getVersion()[0]
	thumb = video_item.getImage() if video_item.getImage() else u'DefaultVideo.png'
	title = video_item.getTitle() if video_item.getTitle() else video_item.getName()
	fanart = ''
	settings = context.getSettings()
	item = xbmcgui.ListItem(label=title)
	if video_item.getFanart() and settings.showFanart():
		fanart = video_item.getFanart()
	if major_version <= 12:
		item.setIconImage(thumb)
		item.setProperty("Fanart_Image", fanart)
	elif major_version <= 15:
		item.setArt({'thumb': thumb, 'fanart': fanart})
		item.setIconImage(thumb)
	else:
		item.setArt({'icon': thumb, 'thumb': thumb, 'fanart': fanart})
	if video_item.getContextMenu() is not None:
		item.addContextMenuItems(video_item.getContextMenu(), replaceItems=video_item.getReplaceContextMenu())
	if video_item.getUseDash() and settings.getDashSupportAddon():
		item.setProperty('inputstreamaddon', 'inputstream.adaptive')
		item.setProperty('inputstream.adaptive.manifest_type', 'mpd')
	item.setProperty(u'IsPlayable', u'true')
	if video_item.subtitles:
		item.setSubtitles(video_item.subtitles)
	_info_labels = InfoLabels.createFromItem(context, video_item)
	# This should work for all versions of XBMC/KODI.
	if 'duration' in _info_labels:
		duration = _info_labels['duration']
		del _info_labels['duration']
		item.addStreamInfo('video', {'duration': duration})
	item.setInfo(type=u'video', infoLabels=_info_labels)
	return item

def to_audio_item(context, audio_item):
	context.debug('Converting AudioItem')
	major_version = context.getSystemVersion().getVersion()[0]
	thumb = audio_item.getImage() if audio_item.getImage() else u'DefaultAudio.png'
	title = audio_item.getName()
	fanart = ''
	settings = context.getSettings()
	item = xbmcgui.ListItem(label=title)
	if audio_item.getFanart() and settings.showFanart():
		fanart = audio_item.getFanart()
	if major_version <= 12:
		item.setIconImage(thumb)
		item.setProperty("Fanart_Image", fanart)
	elif major_version <= 15:
		item.setArt({'thumb': thumb, 'fanart': fanart})
		item.setIconImage(thumb)
	else:
		item.setArt({'icon': thumb, 'thumb': thumb, 'fanart': fanart})
	if audio_item.getContextMenu() is not None:
		item.addContextMenuItems(audio_item.getContextMenu(), replaceItems=audio_item.getReplaceContextMenu())
	item.setProperty(u'IsPlayable', u'true')
	item.setInfo(type=u'music', infoLabels=InfoLabels.createFromItem(context, audio_item))
	return item

def to_uri_item(context, base_item):
	context.debug('Converting UriItem')
	item = xbmcgui.ListItem(path=base_item.getUri())
	item.setProperty(u'IsPlayable', u'true')
	return item

def to_item(context, base_item):
	if isinstance(base_item, UriItem):
		return to_uri_item(context, base_item)
	if isinstance(base_item, VideoItem):
		return to_video_item(context, base_item)
	if isinstance(base_item, AudioItem):
		return to_audio_item(context, base_item)
	return None
