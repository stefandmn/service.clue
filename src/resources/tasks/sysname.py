# -*- coding: utf-8 -*-

import os
import common
from .abcwindow import WindowTask



class SystemName(WindowTask):
	key = "sysname"


	def code(self):
		return self.key


	def load(self):
		data = self._get()
		self.debug("Collected host data: %s" % str(data))
		self.set(1201, data)


	def onClick_1202(self):
		self._lock()
		data = self.get(1201)
		if data is not None:
			self._set(data)
		self._unlock()
		self.dispose()


	def _get(self):
		(_status, _content) = self._process('/bin/hostname')
		data = _content if _status and _content is not None and _content != "" else None
		return data


	def _set(self, data):
		# change system hostname
		hostname = open('/proc/sys/kernel/hostname', 'w')
		hostname.write(data)
		hostname.close()
		hostname = open('%s/hostname' % self.CONFIG_CACHE, 'w')
		hostname.write(data)
		hostname.close()
		# adap hosts file
		hosts = open('/etc/hosts', 'w')
		user_hosts_file = self.HOME + '/.config/hosts.conf'
		if os.path.isfile(user_hosts_file):
			user_hosts = open(user_hosts_file, 'r')
			hosts.write(user_hosts.read())
			user_hosts.close()
		hosts.write('127.0.0.1\tlocalhost %s\n' %data)
		hosts.write('::1\tlocalhost ip6-localhost ip6-loopback %s\n' %data)
		hosts.close()
		# update Kodi device name
		common.setSystemSetting("services.devicename", data)
