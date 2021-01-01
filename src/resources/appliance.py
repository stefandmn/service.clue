# -*- coding: utf-8 -*-

import os
import crypt
import common
import subprocess



class System:
	HOME = os.environ['HOME']
	CONFIG_CACHE = os.environ.get('CONFIG_CACHE', '%s/.cache' % HOME)
	USER_CONFIG = os.environ.get('USER_CONFIG', '%s/.config' % HOME)


	def method(self, cls, mtd, *args, **kwargs):
		if cls is not None and cls != '' and mtd is not None and mtd != '':
			return common.clscall(cls, mtd, *args, **kwargs)
		else:
			return None


	def function(self, fnc, *args, **kwargs):
		if fnc is not None and fnc != '':
			return common.funcall(fnc, *args, **kwargs)
		else:
			return None


	def process(self, cmd):
		if cmd is not None and cmd != '':
			return common.procexec(cmd)
		else:
			return None


	def any2int(self, v, error=False, none=True):
		return common.any2int(v, error=error, none=none)


	def any2float(self, v, error=False, none=True):
		return common.any2float(v, error=error, none=none)


	def any2str(self, v, error=False, none=True):
		return common.any2str(v, error=error, none=none)


	def any2bool(self, v, error=False, none=True):
		return common.any2bool(v, error=error, none=none)


	def trace(self, txt, code=None):
		common.trace(txt, code=code)


	def debug(self, txt, code=None):
		common.debug(txt, code=code)


	def info(self, txt, code=None):
		common.info(txt, code=code)


	def notice(self, txt, code=None):
		common.notice(txt, code=code)


	def warn(self, txt, code=None):
		common.warn(txt, code=code)


	def error(self, txt, code=None):
		common.error(txt, code=code)


	def translate(self, code):
		return common.translate(code)


	def check_root_access(self, pwd):
		if pwd:
			stream = os.popen('more /etc/shadow | grep root')
			output = stream.read()
			password = output.split(':')[1]
			self.trace("Found encoded password: %s" %password)
			hashcode = password[0:password.find('$',3)+1]
			self.trace("Calculated has code based on hashing method SHA-512: %s" %hashcode)
			inputpwd = crypt.crypt(pwd, hashcode)
			self.trace("Encrypted input password: %s" %inputpwd)
			if inputpwd != password:
				raise RuntimeError("Password doesn't match")
		else:
			self.debug("No password provided")


	def set_root_password(self, pwd1, pwd2):
		if pwd1 and pwd2:
			shell = subprocess.Popen(["passwd"], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)
			readout1 = shell.stdout.readline()
			self.debug("Command executed, output: %s" %readout1)
			try:
				shell.stdin.write('%s\n' % pwd1)
				readout2 = shell.stdout.readline()
				self.debug("Input submitted, second output: %s" %readout2)
			except:
				readout2 = shell.stdout.readline()
				shell.communicate()
				raise RuntimeError(readout2)
			try:
				shell.stdin.write('%s\n' % pwd2)
				readout3 = shell.stdout.readline()
				self.debug("Input submitted, third output: %s" % readout3)
			except:
				readout3 = shell.stdout.readline()
				shell.communicate()
				raise RuntimeError(readout3)
			outs, errs = shell.communicate()
			code = shell.returncode
			self.debug("Results of [passwd] system command execution: code=%s, stdout=%s, strerr=%s" %(str(code),str(outs),str(errs)))
		else:
			self.debug("No password provided")



class Identity(System):


	def get_hostname(self):
		# read the hostname running an external process
		(_status, _content) = self.process('/bin/hostname')
		data = _content if _status and _content is not None and _content != "" else None
		return data


	def get_devicename(self):
		return common.getSystemSetting("services.devicename")


	def set_hostname(self, name):
		# change system hostname
		hostname = open('/proc/sys/kernel/hostname', 'w')
		hostname.write(name)
		hostname.close()
		hostname = open('%s/hostname' % self.CONFIG_CACHE, 'w')
		hostname.write(name)
		hostname.close()
		# adap hosts file
		hosts = open('/etc/hosts', 'w')
		user_hosts_file = self.HOME + '/.config/hosts.conf'
		if os.path.isfile(user_hosts_file):
			user_hosts = open(user_hosts_file, 'r')
			hosts.write(user_hosts.read())
			user_hosts.close()
		hosts.write('127.0.0.1\tlocalhost %s\n' % name)
		hosts.write('::1\tlocalhost ip6-localhost ip6-loopback %s\n' % name)
		hosts.close()


	def set_device(self, name):
		# update Kodi device name
		common.setSystemSetting("services.devicename", name)


	def set_identity(self, name):
		self.set_hostname(name)
		self.set_device(name)



class Services(Identity):


	def get_sysservice_status(self, service):
		(_status, _content) = self.process("/usr/bin/systemctl is-active %s" % service)
		if _status and _content is not None and _content == "active":
			return True
		else:
			return False


	def start_sysservice(self, service):
		self.process("/usr/bin/systemctl start %s" % service)
		return self.get_sysservice_status(service)


	def stop_sysservice(self, service):
		self.process("/usr/bin/systemctl stop %s" % service)
		return not self.get_sysservice_status(service)


	def restart_sysservice(self, service):
		self.process("/usr/bin/systemctl restart %s" % service)
		return self.get_sysservice_status(service)


	def get_appservice_option(self, service, option, default=None):
		conf_file_name = ''
		if os.path.exists('%s/services/%s.conf' % (self.CONFIG_CACHE, service)):
			conf_file_name = '%s/services/%s.conf' % (self.CONFIG_CACHE, service)
		elif os.path.exists('%s/services/%s.disabled' % (self.CONFIG_CACHE, service)):
			conf_file_name = '%s/services/%s.disabled' % (self.CONFIG_CACHE, service)
		if os.path.exists(conf_file_name):
			with open(conf_file_name, 'r') as conf_file:
				for line in conf_file:
					if option in line:
						if '=' in line:
							default = line.strip().split('=')[-1]
		return default


	def set_appservice_option(self, service, option, value):
		lines = []
		changed = False
		conf_file_name = '%s/services/%s.conf' % (self.CONFIG_CACHE, service)
		if os.path.isfile(conf_file_name):
			with open(conf_file_name, 'r') as conf_file:
				for line in conf_file:
					if option in line:
						line = '%s=%s' % (option, value)
						changed = True
					lines.append(line.strip())
		if changed == False:
			lines.append('%s=%s' % (option, value))
		with open(conf_file_name, 'w') as conf_file:
			conf_file.write('\n'.join(lines) + '\n')


	def get_appservice_status(self, service):
		if self.get_sysservice_status(service):
			if os.path.exists('%s/services/%s.conf' % (self.CONFIG_CACHE, service)):
				return True
		return False


	def enable_appservice(self, service):
		if not os.path.exists('%s/services/%s.conf' % (self.CONFIG_CACHE, service)):
			if os.path.exists('%s/services/%s.disabled' % (self.CONFIG_CACHE, service)):
				os.rename('%s/services/%s.disabled' % (self.CONFIG_CACHE, service), '%s/services/%s.conf' % (self.CONFIG_CACHE, service))
			else:
				os.replace('/usr/share/services/%s.conf' %service, '%s/services/%s.conf' % (self.CONFIG_CACHE, service))
		if os.path.exists('%s/services/%s.conf' % (self.CONFIG_CACHE, service)):
			return self.start_sysservice(service)
		else:
			return False


	def disable_appservice(self, service):
		self.stop_sysservice(service)
		if os.path.exists('%s/services/%s.conf' % (self.CONFIG_CACHE, service)):
			os.rename('%s/services/%s.conf' % (self.CONFIG_CACHE, service), '%s/services/%s.disabled' % (self.CONFIG_CACHE, service))
		if not os.path.exists('%s/services/%s.conf' % (self.CONFIG_CACHE, service)):
			return not self.get_sysservice_status(service)
		else:
			return False



class Clue(Services):
	pass