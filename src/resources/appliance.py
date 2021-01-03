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


	def hwtype(self):
		_status, _output = self.process('uname -m')
		if _status:
			return _output
		else:
			self.error("Error reading hardware type: %s" %_output)
			return None


	def kernelversion(self):
		_status, _output = self.process('uname -r')
		if _status:
			return _output
		else:
			self.error("Error reading kernel version: %s" %_output)
			return None


	def chipset(self):
		_status, _output = self.process('cat /proc/cpuinfo | grep Hardware | cut -d":" -f2 | tr -d " "')
		if _status:
			return _output
		else:
			self.error("Error reading chipset: %s" %_output)
			return None


	def serialnumber(self):
		_status, _output = self.process('cat /proc/cpuinfo | grep Serial | cut -d":" -f2 | tr -d " "')
		if _status:
			return _output
		else:
			self.error("Error reading serial number: %s" %_output)
			return None


	def model(self):
		_model = None
		_status, _output = self.process('grep Revision /proc/cpuinfo | cut -d " " -f 2 | sed "s/^1000//"')
		if _status:
			if _output == "0002": 
				model = "B"
			elif _output == "0003":
				model = "B"
			elif _output == "0004":
				model = "B"
			elif _output == "0005":
				model = "B"
			elif _output == "0006":
				model = "B"
			elif _output == "0007":
				model = "A"
			elif _output == "0008":
				model = "A"
			elif _output == "0009":
				model = "A"
			elif _output == "000d":
				model = "B"
			elif _output == "000e":
				model = "B"
			elif _output == "000f":
				model = "B"
			elif _output == "0010":
				model = "B+"
			elif _output == "0011":
				model = "Compute Module 1"
			elif _output == "0012":
				model = "A+"
			elif _output == "0013":
				model = "B+"
			elif _output == "0014":
				model = "Compute Module 1 (Embest, China)"
			elif _output == "0015":
				model = "A+ (Embest, China)"
			elif _output == "a01040":
				model = "2 Model B"
			elif _output == "a01041":
				model = "2 Model B (Sony, UK)"
			elif _output == "a21041":
				model = "2 Model B (Embest, China)"
			elif _output == "a22042":
				model = "2 Model B+"
			elif _output == "900021":
				model = "A+"
			elif _output == "900032":
				model = "B+"
			elif _output == "900092":
				model = "Zero"
			elif _output == "900093":
				model = "Zero"
			elif _output == "920093":
				model = "Zero"
			elif _output == "9000c1":
				model = "Zero W"
			elif _output == "a02082":
				model = "3 Model B (Sony, UK)"
			elif _output == "a020a0":
				model = "Compute Module 3 (Lite)"
			elif _output == "a22082":
				model = "3 Model B (Embest, China)"
			elif _output == "a32082":
				model = "3 Model B (Sony, Japan)"
			elif _output == "a52082":
				model = "3 Model B (Stadium, UK)"
			elif _output == "a22083":
				model = "3 Model B (Embest, China)"
			elif _output == "a03111":
				model = "4 (Sony, UK)"
			elif _output == "b03111":
				model = "4 (Sony, UK)"
			elif _output == "c03111":
				model = "4 (Sony, UK)"
			else:
				model = "unknown (%s)" %_output
			return model
		else:
			self.error("Error reading device model: %s" %_output)
			return None


	def cputemp(self):
		_status, _output = self.process('/opt/vc/bin/vcgencmd measure_temp | cut -c "6-9"')
		if _status:
			return _output
		else:
			self.error("Error reading CPU temperature: %s" % _output)
			return None


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
			return True
		else:
			self.debug("No password provided")
			return False


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
			return code == 0
		else:
			self.debug("No password provided")
			return False


	def get_property(self, conf_file_name, option, default=None):
		if os.path.exists(conf_file_name):
			with open(conf_file_name, 'r') as conf_file:
				for line in conf_file:
					if line != '' and line.strip().startswith(option):
						if '=' in line:
							if line.strip().split('=')[0].strip() == option.strip():
								default = line.strip().split('=')[-1].strip()
			conf_file.close()
		return default


	def set_property(self, conf_file_name, option, value):
		lines = []
		changed = False
		ignored = False
		if os.path.isfile(conf_file_name):
			if value is None or value == "":
				usecase = -1
			elif value == "#":
				usecase = 0
			else:
				usecase = 1
				value = str(value)
			with open(conf_file_name, 'r') as conf_file:
				for line in conf_file:
					if usecase == 1:
						if line != '' and (line.strip().startswith(option) or (line.strip().startswith('#') and line.strip()[1:].strip().startswith(option))):
							if '=' in line:
								if line.strip().split('=')[0].strip() == option.strip():
									line = '%s=%s' % (option, value)
									changed = True
					elif usecase == 0:
						if line != '' and (line.strip().startswith(option)):
							if '=' in line:
								if line.strip().split('=')[0].strip() == option.strip():
									line = '# ' + line
									changed = True
					elif usecase == -1:
						if line != '' and (line.strip().startswith(option)):
							if '=' in line:
								if line.strip().split('=')[0].strip() == option.strip():
									ignored = True
									changed = True
					if not ignored:
						lines.append(line.strip())
					else:
						ignored = False
			conf_file.close()
			if not changed and usecase == 1:
				lines.append('%s=%s' % (option, value))
			with open(conf_file_name, 'w') as conf_file:
				conf_file.write('\n'.join(lines))
				conf_file.write("\n")
			conf_file.close()
		else:
			self.error("Configuration file not found: %s" %conf_file_name)


	def remount_boot(self, write=False):
		if write:
			flag = "rw"
		else:
			flag = "ro"
		_status, _output = self.process('mount -o remount,%s /dev/mmcblk0p1 /boot' %flag)
		if _status:
			if _output is not None and _output != '':
				self.trace("Remount of /boot partition: %s" %_output)
		else:
			self.error("Error executing remount of /boot partition: %s" %_output)



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
		return self.get_property(conf_file_name, option=option, default=default)


	def set_appservice_option(self, service, option, value):
		conf_file_name = '%s/services/%s.conf' % (self.CONFIG_CACHE, service)
		self.set_property(conf_file_name, option=option, value=value)


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
	FILE_BOOT_CONFIG = "/boot/config.txt"
	PROP_GPU_MEM = "gpu_mem"
	PROP_ARM_FREQ = "arm_freq"
	PROP_CORE_FREQ = "core_freq"
	PROP_SDRAM_FREQ = "sdram_freq"
	PROP_OVERVOLTAGE = "over_voltage"
	PROP_FORCE_TURBO = "force_turbo"


	def get_gpu_memorysplit(self):
		return self.get_property(self.FILE_BOOT_CONFIG, self.PROP_GPU_MEM, 128)


	def set_gpu_memorysplit(self, memory):
		self.remount_boot(True)
		self.set_property(self.FILE_BOOT_CONFIG, self.PROP_GPU_MEM, memory)
		self.remount_boot(False)


	def get_overclocking_profiles(self):
		_profiles = []
		if self.hwtype() == "armv6l":
			_profiles = ["None", "Modest", "Medium", "High", "Turbo"]
		elif self.hwtype() == "armv7l":
			_profiles = ["None", "High"]
		return _profiles


	def get_currentoverclocking_profile(self):
		_profile = None
		_hwtype = self.hwtype()
		_freq = self.get_property("/boot/config.txt", "arm_freq")
		if _hwtype == "armv6l":
			if _freq is None:
				_profile = "None"
			elif _freq == "700":
				_profile= "None"
			elif _freq == "800":
				_profile= "Modest"
			elif _freq == "900":
				_profile= "Medium"
			elif _freq == "950":
				_profile= "High"
			elif _freq == "1000":
				_profile= "Turbo"
			else:
				self.warn("Unknown frequency to recognize the overclocking profile: %s" % str(_freq))
				_profile = "Unknown"
		elif _hwtype == "armv7l":
			if _freq is None:
				_profile = "None"
			elif _freq == "900":
				_profile= "None"
			elif _freq == "1000":
				_profile= "High"
			else:
				_profile = "Unknown"
				self.warn("Unknown frequency to recognize the overclocking profile: %s" % str(_freq))
		else:
			_profile = "Unknown"
			self.warn("Unknown hardware type to identify the overclocking profile: %s" % str(_hwtype))
		return _profile


	def set_overclocking_profile(self, profile):
		_hwtype = self.hwtype()
		if _hwtype == "armv6l":
			self.remount_boot(True)
			if profile is None or profile == "None":
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_ARM_FREQ, 700)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_CORE_FREQ, 250)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_SDRAM_FREQ, 400)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_OVERVOLTAGE, 0)
			elif profile == "Modest":
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_ARM_FREQ, 800)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_CORE_FREQ, 250)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_SDRAM_FREQ, 400)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_OVERVOLTAGE, 0)
			elif profile == "Medium":
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_ARM_FREQ, 900)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_CORE_FREQ, 250)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_SDRAM_FREQ, 450)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_OVERVOLTAGE, 2)
			elif profile == "High":
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_ARM_FREQ, 950)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_CORE_FREQ, 250)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_SDRAM_FREQ, 450)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_OVERVOLTAGE, 6)
			elif profile == "Turbo":
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_ARM_FREQ, 1000)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_CORE_FREQ, 500)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_SDRAM_FREQ, 600)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_OVERVOLTAGE, 6)
			else:
				self.warn("Unknown overclocking profile to apply: %s" %str(profile))
			self.remount_boot(False)
		elif _hwtype == "armv7l":
			self.remount_boot(True)
			if profile is None or profile == "None":
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_ARM_FREQ, 900)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_CORE_FREQ, 250)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_SDRAM_FREQ, 450)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_OVERVOLTAGE, 0)
			elif profile == "High":
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_ARM_FREQ, 1000)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_CORE_FREQ, 500)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_SDRAM_FREQ, 500)
				self.set_property(self.FILE_BOOT_CONFIG, self.PROP_OVERVOLTAGE, 2)
			else:
				self.warn("Unknown overclocking profile to apply: %s" % str(profile))
			self.remount_boot(False)
		else:
			self.warn("Unknown hardware type to apply the overclocking profile: %s" % str(_hwtype))


	def get_turbomode(self):
		return self.any2bool(self.get_property(self.FILE_BOOT_CONFIG, self.PROP_FORCE_TURBO))


	def set_turbomode(self, value):
		self.remount_boot(True)
		if value:
			self.set_property(self.FILE_BOOT_CONFIG, self.PROP_FORCE_TURBO, 1)
			self.set_property(self.FILE_BOOT_CONFIG, self.PROP_ARM_FREQ, None)
			self.set_property(self.FILE_BOOT_CONFIG, self.PROP_CORE_FREQ, None)
			self.set_property(self.FILE_BOOT_CONFIG, self.PROP_SDRAM_FREQ, None)
			self.set_property(self.FILE_BOOT_CONFIG, self.PROP_OVERVOLTAGE, None)
		else:
			self.set_property(self.FILE_BOOT_CONFIG, self.PROP_FORCE_TURBO, 0)
		self.remount_boot(False)