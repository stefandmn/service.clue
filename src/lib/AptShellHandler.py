# -*- coding: utf-8 -*-

from CommonFunctions import *

try:
	from subprocess import check_output
	from subprocess import call
except:
	info('Subprocess import error', "SystemUpdate")


class AptShellHandler:

	_pwd = ""

	def __init__(self, usesudo=False):
		self.sudo = usesudo

	def _CheckVersions(self, package, update=True):
		_cmd = "apt-cache policy " + package
		if update and not self._UpdateCache():
			return False, False
		try:
			result = check_output([_cmd], shell=True).split("\n")
		except Exception as err:
			error("Exception while executing shell command %s: %s" %(_cmd, err), "SystemUpdate")
			return False, False
		if result[0].replace(":", "") == package:
			installed = result[1].split()[1]
			candidate = result[2].split()[1]
			if installed == "(none)":
				installed = False
			if candidate == "(none)":
				candidate = False
			return installed, candidate
		else:
			error("Error during version check", "SystemUpdate")
			return False, False

	def _UpdateCache(self):
		_cmd = 'apt-get update'
		try:
			if self.sudo:
				x = check_output('echo \'%s\' | sudo -S %s' %(self._getPassword(), _cmd), shell=True)
			else:
				x = check_output(_cmd.split())
		except Exception as err:
			error("Exception while executing shell command %s: %s" %(_cmd, err), "SystemUpdate")
			return False

		return True

	#Returns True if newer package is available in the repositories
	def CheckUpgradeAvailable(self, package):
		installed, candidate = self._CheckVersions(package)
		if installed and candidate:
			if installed != candidate:
				debug("Package '%s' is currently version '%s' but it is available also for version '%s'" %(package, installed, candidate))
				return True
			else:
				debug("Already on newest version of '%s' package" %package, "SystemUpdate")
				return False
		elif not installed:
				debug("No version installed of '%s' package" %package, "SystemUpdate")
				return False
		else:
			return False

	def UpgradePackage(self, package):
		_cmd = "apt-get install -y " + package
		try:
			if self.sudo:
				x = check_output('echo \'%s\' | sudo -S %s' %(self._getPassword(), _cmd), shell=True)
			else:
				x = check_output(_cmd.split())
			info("Upgrade successful", "SystemUpdate")
		except Exception as err:
			error("Exception while executing shell command %s: %s" %(_cmd, err), "SystemUpdate")
			return False
		return True

	def UpgradeSystem(self):
		_cmd = "apt-get upgrade -y"
		try:
			info("Upgrading system", "SystemUpdate")
			if self.sudo:
				x = check_output('echo \'%s\' | sudo -S %s' %(self._getPassword(), _cmd), shell=True)
			else:
				x = check_output(_cmd.split())
		except Exception as err:
			error("Exception while executing shell command %s: %s" %(_cmd, err), "SystemUpdate")
			return False
		return True

	def _getPassword(self):
		if len(self._pwd) == 0:
			self._pwd = PasswordDialog()
		return self._pwd
