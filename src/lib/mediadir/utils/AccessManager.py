# -*- coding: utf-8 -*-

import hashlib
import time


class AccessManager(object):
	def __init__(self, settings):
		self._settings = settings

	def hasLoginCredentials(self):
		"""
		Returns True if we have a username and password.
		:return: True if username and password exists
		"""
		username = self._settings.getString('login.username', '')
		password = self._settings.getString('login.password', '')
		return username != '' and password != ''

	def removeLoginCredentials(self):
		self._settings.setString('login.username', '')
		self._settings.setString('login.password', '')

	def getLoginCredentials(self):
		"""
		Returns the username and password (Tuple)
		:return: (username, password)
		"""
		username = self._settings.getString('login.username', '')
		password = self._settings.getString('login.password', '')
		return username, password

	def isNewLoginCredential(self, update_hash=True):
		"""
		Returns True if username or/and password are new.
		:return:
		"""
		username = self._settings.getString('login.username', '')
		password = self._settings.getString('login.password', '')
		m = hashlib.md5()
		m.update(username.encode('utf-8')+password.encode('utf-8'))
		current_hash = m.hexdigest()
		old_hash = self._settings.getString('login.hash', '')
		if current_hash != old_hash:
			if update_hash:
				self._settings.setString('login.hash', current_hash)
			return True

		return False

	def getAccessToken(self):
		"""
		Returns the access token for some API
		:return: access_token
		"""
		return self._settings.getString('access_token', '')

	def getRefreshToken(self):
		"""
		Returns the refresh token
		:return: refresh token
		"""
		return self._settings.getString('refresh_token', '')

	def hasRefreshToken(self):
		return self.getRefreshToken() != ''

	def isAccessTokenExpired(self):
		"""
		Returns True if the access_token is expired otherwise False.
		If no expiration date was provided and an access_token exists
		this method will always return True
		:return:
		"""
		# with no access_token it must be expired
		if not self._settings.getString('access_token', ''):
			return True
		# in this case no expiration date was set
		expires = self._settings.getInt('access_token.expires', -1)
		if expires == -1:
			return False
		now = int(time.time())
		return expires <= now

	def updateAccessToken(self, access_token, unix_timestamp=None, refresh_token=None):
		"""
		Updates the old access token with the new one.
		:param access_token:
		:return:
		"""
		self._settings.setString('access_token', access_token)
		if unix_timestamp is not None:
			self._settings.setInt('access_token.expires', int(unix_timestamp))
		if refresh_token is not None:
			self._settings.setString('refresh_token', refresh_token)
		pass
