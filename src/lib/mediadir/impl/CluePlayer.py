# -*- coding: utf-8 -*-

import sys
from mediadir.AbstractPlayer import AbstractPlayer

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc


class CluePlayer(AbstractPlayer):
	def __init__(self, player_type, context):
		AbstractPlayer.__init__(self)
		self._player_type = player_type
		if player_type == 'audio':
			self._player_type = 'music'
		self._context = context

	def play(self, playlist_index=-1):
		"""
		We call the player in this way, because 'Player.play(...)' will call the addon again while the instance is
		running. This is somehow shitty, because we couldn't release any resources and in our case we couldn't release
		the cache. So this is the solution to prevent a locked database (sqlite).
		"""
		self._context.execute('Playlist.PlayOffset(%s,%d)' % (self._player_type, playlist_index))
		pass

	def stop(self):
		xbmc.Player().stop()
		pass

	def pause(self):
		xbmc.Player().pause()
		pass
