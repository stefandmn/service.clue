# -*- coding: utf-8 -*-

import os
import sys
import common
from .abstract import ServiceRunner



class Hostname(ServiceRunner):


	def code(self):
		return "hostname"


	def run(self, *args):
		params = dict(arg.split("=") for arg in sys.argv[2].split("&"))
		self.debug('Found parameters: %s' % str(params))
		self._function(".".join(["self", params.get('method')]))


	def get(self):
		data = self.__get()
		self.debug("Collected data: %s" %str(data))
		if data is not None:
			common.setSkinProperty(self.windowid, "ClueSetup.Hostname", str(data))


	def set(self):
		data = self.getControlValue(1201)
		if data is not None:
			self.__set(data)


	def __get(self):
		(_status, _content) = self._process('/bin/hostname')
		if _status and _content is not None and _content != "":
			return _content
		else:
			return None


	def __set(self, data):
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
		common.setSystemSessing("services.devicename", data)
