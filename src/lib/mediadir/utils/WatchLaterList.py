# -*- coding: utf-8 -*-

import datetime
from .ItemCast import to_json, from_json
from .StorageData import StorageData


class WatchLaterList(StorageData):
	def __init__(self, filename):
		StorageData.__init__(self, filename)

	def clear(self):
		self._clear()

	def list(self):
		result = []
		for key in self._get_ids():
			data = self._get(key)
			item = from_json(data[0])
			result.append(item)
		#
		# inner function for sorting
		def _sort(video_item):
			return video_item.getDate()
		#
		self.sync()
		sorted_list = sorted(result, key=_sort, reverse=False)
		return sorted_list

	def add(self, base_item):
		now = datetime.datetime.now()
		base_item.setDate(now.year, now.month, now.day, now.hour, now.minute, now.second)
		item_json_data = to_json(base_item)
		self._set(base_item.getId(), item_json_data)

	def remove(self, base_item):
		self._remove(base_item.getId())
