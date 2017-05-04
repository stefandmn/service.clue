# -*- coding: utf-8 -*-

from CommonFunctions import *

try:
	import apt
	from aptdaemon import client
	from aptdaemon import errors
except Exception as err:
	error('Python APT import error: %s' %str(err), "SystemUpdate")


class AptDaemonHandler:

	def __init__(self, package=''):
		self.aptclient = client.AptClient()

	def _CheckVersions(self, package):
		if not self._UpdateCache():
			return False, False
		try:
			trans = self.aptclient.upgrade_packages([package])
			trans.simulate(reply_handler=self._aptTransStarted, error_handler=self._aptErrorHandler)
			pkg = trans.packages[4][0]
			if pkg == package:
				cache=apt.Cache()
				cache.open(None)
				cache.upgrade()
				if cache[pkg].installed:
					return cache[pkg].installed.version, cache[pkg].candidate.version
			return False, False
		except Exception as error:
			info("Exception while checking versions: %s" %error, "SystemUpdate")
			return False, False

	def _UpdateCache(self):
		try:
			if self.aptclient.update_cache(wait=True) == "exit-success":
				return True
			else:
				return False
		except errors.NotAuthorizedError:
			error("You are not allowed to update the cache", "SystemUpdate")
			return False
		except Exception as err:
			info("Exception while checking versions: %s" %err, "SystemUpdate")
			return False

	# Returns True if newer package is available in the repositories
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
		try:
			info("Installing new version", "SystemUpdate")
			if self.aptclient.upgrade_packages([package], wait=True) == "exit-success":
				info("Upgrade successful", "SystemUpdate")
				return True
		except Exception as err:
			error("Exception during upgrade: %s" %err, "SystemUpdate")
		return False

	def UpgradeSystem(self):
		try:
			info("Upgrading system", "SystemUpdate")
			if self.aptclient.UpgradeSystem(wait=True) == "exit-success":
				return True
		except Exception as err:
			error("Exception during system upgrade: %s" %err, "SystemUpdate")
		return False

	def _getPassword(self):
		if len(self._pwd) == 0:
			self._pwd = PasswordDialog()
		return self._pwd

	def _aptTransStarted(self):
		pass

	def _aptErrorHandler(self, err):
		error("Apt Error %s" %err, "SystemUpdate")
