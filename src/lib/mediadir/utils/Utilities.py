# -*- coding: utf-8 -*-

__all__ = ['createPath', 'createUriPath', 'stripHtmlFromText', 'findBestFit', 'to_utf8', 'to_unicode', 'getSelectedStream']

import re
import urllib


def to_utf8(text):
	result = text
	if isinstance(text, unicode):
		result = text.encode('utf-8')
	return result

def to_unicode(text):
	result = text
	if isinstance(text, str):
		result = text.decode('utf-8')
	return result

def findBestFit(data, compare_method=None):
	result = None
	last_fit = -1
	if isinstance(data, dict):
		for key in data.keys():
			item = data[key]
			fit = abs(compare_method(item))
			if last_fit == -1 or fit < last_fit:
				last_fit = fit
				result = item
	elif isinstance(data, list):
		for item in data:
			fit = abs(compare_method(item))
			if last_fit == -1 or fit < last_fit:
				last_fit = fit
				result = item
	return result

def getSelectedStream(context, stream_data_list, quality_map_override=None):
	# sort - best stream first
	def _sort_stream_data(_stream_data):
		return _stream_data.get('sort', 0)
	video_quality = context.getSettings().getVideoQuality(quality_map_override=quality_map_override)
	# find - best stream first
	def _find_best_fit_video(_stream_data):
		return video_quality - _stream_data.get('video', {}).get('height', 0)
	sorted_stream_data_list = sorted(stream_data_list, key=_sort_stream_data, reverse=True)
	context.debug('selectable streams: %d' % len(sorted_stream_data_list))
	for sorted_stream_data in sorted_stream_data_list:
		context.debug('selectable stream: %s' % sorted_stream_data)
	selected_stream_data = None
	if context.getSettings().ask4VideoQuality() and len(sorted_stream_data_list) > 1:
		items = []
		for sorted_stream_data in sorted_stream_data_list:
			items.append((sorted_stream_data['title'], sorted_stream_data))
		result = context.getUI().onSelect(context.localize(30010), items)
		if result != -1:
			selected_stream_data = result
	else:
		selected_stream_data = findBestFit(sorted_stream_data_list, _find_best_fit_video)
	if selected_stream_data is not None:
		context.debug('selected stream: %s' % selected_stream_data)
	return selected_stream_data

def createPath(*args):
	comps = []
	for arg in args:
		if isinstance(arg, list):
			return createPath(*arg)
		comps.append(unicode(arg.strip('/').replace('\\', '/').replace('//', '/')))
	uri_path = '/'.join(comps)
	if uri_path:
		return u'/%s/' % uri_path
	return '/'

def createUriPath(*args):
	comps = []
	for arg in args:
		if isinstance(arg, list):
			return createUriPath(*arg)
		comps.append(arg.strip('/').replace('\\', '/').replace('//', '/').encode('utf-8'))
	uri_path = '/'.join(comps)
	if uri_path:
		return urllib.quote('/%s/' % uri_path)
	return '/'

def stripHtmlFromText(text):
	"""
	Removes html tags
	:param text: html text
	:return:
	"""
	return re.sub('<[^<]+?>', '', text)
