# -*- coding: utf-8 -*-

from .StorageData import StorageData
from .ItemCast import to_json, from_json


class FavoriteList(StorageData):
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
		def _sort(_item):
			return _item.getName().upper()
		return sorted(result, key=_sort, reverse=False)

	def add(self, base_item):
		item_json_data = to_json(base_item)
		self._set(base_item.getId(), item_json_data)

	def remove(self, base_item):
		self._remove(base_item.getId())
