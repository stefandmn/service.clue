# -*- coding: utf-8 -*-

import os
import sys
import time
import socket
import hashlib
import string
import CommonFunctions as common

import xbmc
import xbmcvfs
import xbmcaddon

try:
	import sqlite
except:
	pass
try:
	import sqlite3
except:
	pass


# Check if this module should be run in instance mode or not.
__workersByName = {}


class StorageServer():
	def __init__(self, table=None, timeout=24, instance=False):
		self.instance = instance
		self.die = False
		self.settings = xbmcaddon.Addon()
		self.path = xbmc.translatePath('special://temp/')
		if not xbmcvfs.exists(self.path.decode('utf8', 'ignore')):
			self.debug("Making path structure: " + self.path)
			xbmcvfs.mkdir(self.path)
		self.path = os.path.join(self.path, 'Cache.db')

		self.socket = ""
		self.clientsocket = False
		self.sql2 = False
		self.sql3 = False
		self.abortRequested = False
		self.daemon_start_time = time.time()
		if self.instance:
			self.idle = int(self.settings.getSetting("cacheserver_timeout"))
		else:
			self.idle = 3

		self.platform = sys.platform
		self.modules = sys.modules
		self.network_buffer_size = 4096

		if isinstance(table, str) and len(table) > 0:
			self.table = ''.join(c for c in table if c in "%s%s" % (string.ascii_letters, string.digits))
			self.debug("Setting table to: %s" % self.table)
		elif table != False:
			self.debug("No table defined")

		self.setCacheTimeout(timeout)


	def _StartDatabase(self):
		try:
			if "sqlite3" in self.modules:
				self.sql3 = True
				self.debug("Sqlite3 found: " + self.path)
				self.conn = sqlite3.connect(self.path, check_same_thread=False)
			elif "sqlite" in self.modules:
				self.sql2 = True
				self.debug("Sqlite2 found: " + self.path)
				self.conn = sqlite.connect(self.path)
			else:
				self.debug("No sql engine found")
				return False

			self.curs = self.conn.cursor()
			return True
		except Exception, e:
			self.error("Exception: " + repr(e))
			xbmcvfs.delete(self.path)
			return False


	def _Aborting(self):
		if self.instance:
			if self.die:
				return True
		else:
			return xbmc.abortRequested
		return False


	def _SocketInit(self, check_stale=False):
		if not self.socket or check_stale:
			self.debug("Checking socket")
			if self.platform == "win32" or xbmc.getCondVisibility('system.platform.android'):
				self.debug("Creating socket for Windows/Android platform")
				port = self.settings.getSetting("cacheserver_port")
				self.socket = ("127.0.0.1", int(port))
			else:
				self.debug("Creating POSIX socket")
				self.socket = os.path.join(xbmc.translatePath('special://temp/').decode("utf-8"), 'cache.socket')
				if xbmcvfs.exists(self.socket) and check_stale:
					self.debug("Deleting stale socket file: " + self.socket)
					xbmcvfs.delete(self.socket)
		self.info("Socket initialized: " + repr(self.socket))


	def _ReceiveData(self):
		data = self._recv(self.clientsocket)
		try:
			data = eval(data)
		except:
			self.warn("Couldn't evaluate message: " + repr(data))
			data = {"action": "stop"}
		return data


	def _RunCommand(self, data):
		res = ""
		if data["action"] == "get":
			res = self._sqlGet(data["table"], data["name"])
		elif data["action"] == "get_multi":
			res = self._sqlGetMulti(data["table"], data["name"], data["items"])
		elif data["action"] == "set_multi":
			res = self._sqlSetMulti(data["table"], data["name"], data["data"])
		elif data["action"] == "set":
			res = self._sqlSet(data["table"], data["name"], data["data"])
		elif data["action"] == "del":
			res = self._sqlDel(data["table"], data["name"])
		elif data["action"] == "lock":
			res = self._lock(data["table"], data["name"])
		elif data["action"] == "unlock":
			res = self._unlock(data["table"], data["name"])
		if len(res) > 0:
			self._send(self.clientsocket, repr(res))


	def _ShowMessage(self, heading, message):
		duration = 10 * 1000
		xbmc.executebuiltin((u'Notification("%s", "%s", %s)' % (heading, message, duration)).encode("utf-8"))


	def _recv(self, sock):
		data = "   "
		idle = True
		i = 0
		start = time.time()
		while data[len(data) - 2:] != "\r\n" or not idle:
			try:
				if idle:
					recv_buffer = sock.recv(self.network_buffer_size)
					idle = False
					i += 1
					data += recv_buffer
					start = time.time()
				elif not idle:
					if data[len(data) - 2:] == "\r\n":
						sock.send("COMPLETE\r\n" + (" " * (15 - len("COMPLETE\r\n"))))
						idle = True
					elif len(recv_buffer) > 0:
						sock.send("ACK\r\n" + (" " * (15 - len("ACK\r\n"))))
						idle = True
					recv_buffer = ""
			except socket.error, e:
				if not e.errno in [10035, 35]:
					self.error("Socket error: " + repr(e))
				if e.errno in [22]:  # We can't fix this.
					return ""
				if start + 10 < time.time():
					self.debug("Receive over time")
					break

		return data.strip()


	def _send(self, sock, data):
		idle = True
		status = ""
		i = 0
		start = time.time()
		while len(data) > 0 or not idle:
			send_buffer = " "
			try:
				if idle:
					if len(data) > self.network_buffer_size:
						send_buffer = data[:self.network_buffer_size]
					else:
						send_buffer = data + "\r\n"
					result = sock.send(send_buffer)
					i += 1
					idle = False
					start = time.time()
				elif not idle:
					status = ""
					while status.find("COMPLETE\r\n") == -1 and status.find("ACK\r\n") == -1:
						status = sock.recv(15)
						i -= 1
					idle = True
					if len(data) > self.network_buffer_size:
						data = data[self.network_buffer_size:]
					else:
						data = ""
			except socket.error, e:
				self.error("Socket error: " + repr(e))
				if e.errno != 10035 and e.errno != 35 and e.errno != 107 and e.errno != 32:
					if start + 10 < time.time():
						self.debug("Send over time")
						break

		return status.find("COMPLETE\r\n") > -1


	def _lock(self, table, name):
		locked = True
		curlock = self._sqlGet(table, name)
		if curlock.strip():
			if float(curlock) < self.daemon_start_time:
				self.debug("Removing stale lock")
				self._sqlExecute("DELETE FROM " + table + " WHERE name = %s", (name,))
				self.conn.commit()
				locked = False
		else:
			locked = False
		if not locked:
			self._sqlExecute("INSERT INTO " + table + " VALUES ( %s , %s )", (name, time.time()))
			self.conn.commit()
			self.debug("Locked: " + name.decode('utf8', 'ignore'))
			return "true"
		self.debug("Failed for: " + name.decode('utf8', 'ignore'))
		return "false"


	def _unlock(self, table, name):
		self._CheckTable(table)
		self._sqlExecute("DELETE FROM " + table + " WHERE name = %s", (name,))
		self.conn.commit()
		return "true"


	def _sqlSetMulti(self, table, pre, inp_data):
		self._CheckTable(table)
		for name in inp_data:
			if self._sqlGet(table, pre + name).strip():
				self.debug("Update: " + pre + name.decode('utf8', 'ignore'))
				self._sqlExecute("UPDATE " + table + " SET data = %s WHERE name = %s", (inp_data[name], pre + name))
			else:
				self.debug("Insert: " + pre + name.decode('utf8', 'ignore'))
				self._sqlExecute("INSERT INTO " + table + " VALUES ( %s , %s )", (pre + name, inp_data[name]))
		self.conn.commit()
		return ""


	def _sqlGetMulti(self, table, pre, items):
		self._CheckTable(table)
		ret_val = []
		for name in items:
			self._sqlExecute("SELECT data FROM " + table + " WHERE name = %s", (pre + name))
			result = ""
			for row in self.curs:
				self.debug("Adding: " + str(repr(row[0]))[0:20])
				result = row[0]
			ret_val += [result]
		self.debug("Returning: " + repr(ret_val))
		return ret_val


	def _sqlSet(self, table, name, data):
		self._CheckTable(table)
		if self._sqlGet(table, name).strip():
			self.debug("Update: " + data.decode('utf8', 'ignore'))
			self._sqlExecute("UPDATE " + table + " SET data = %s WHERE name = %s", (data, name))
		else:
			self.debug("Insert: " + data.decode('utf8', 'ignore'))
			self._sqlExecute("INSERT INTO " + table + " VALUES ( %s , %s )", (name, data))
		self.conn.commit()
		return ""


	def _sqlGet(self, table, name):
		self._CheckTable(table)
		self._sqlExecute("SELECT data FROM " + table + " WHERE name = %s", name)
		for row in self.curs:
			self.debug("Returning: " + str(repr(row[0]))[0:20])
			return row[0]
		self.debug("Returning empty")
		return " "


	def _sqlDel(self, table, name):
		self._CheckTable(table)
		self._sqlExecute("DELETE FROM " + table + " WHERE name LIKE %s", name)
		self.conn.commit()
		return "true"


	def _sqlExecute(self, sql, data):
		try:
			if self.sql2:
				self.curs.execute(sql, data)
			elif self.sql3:
				sql = sql.replace("%s", "?")
				if isinstance(data, tuple):
					self.curs.execute(sql, data)
				else:
					self.curs.execute(sql, (data,))
		except sqlite3.DatabaseError, e:
			if xbmcvfs.exists(self.path) and (str(e).find("file is encrypted") > -1 or str(e).find("not a database") > -1):
				self.debug("Deleting broken database file")
				xbmcvfs.delete(self.path)
				self._StartDatabase()
			else:
				self.debug("Database error, but database NOT deleted: " + repr(e))
		except:
			self.error("Uncaught exception")


	def _CheckTable(self, table):
		try:
			self.curs.execute("create table " + table + " (name text unique, data text)")
			self.conn.commit()
			self.debug("Created new table")
		except:
			pass


	def _Evaluate(self, data):
		try:
			data = eval(data)
			return data
		except:
			self.error("Couldn't evaluate message: " + repr(data))
			return ""


	def _GenerateKey(self, funct, *args):
		name = repr(funct)
		if name.find(" of ") > -1:
			name = name[name.find("method") + 7:name.find(" of ")]
		elif name.find(" at ") > -1:
			name = name[name.find("function") + 9:name.find(" at ")]
		keyhash = hashlib.md5()
		for params in args:
			if isinstance(params, dict):
				for key in sorted(params.iterkeys()):
					if key not in ["new_results_function"]:
						keyhash.update("'%s'='%s'" % (key, params[key]))
			elif isinstance(params, list):
				keyhash.update(",".join(["%s" % el for el in params]))
			else:
				try:
					keyhash.update(params)
				except:
					keyhash.update(str(params))
		name += "|" + keyhash.hexdigest() + "|"
		self.debug("Generate key: " + repr(name))
		return name


	def _getCache(self, name, cache):
		if name in cache:
			if "timeout" not in cache[name]:
				cache[name]["timeout"] = 3600
			if cache[name]["timestamp"] > time.time() - (cache[name]["timeout"]):
				self.debug("Found cache: " + name.decode('utf8', 'ignore'))
				return cache[name]["res"]
			else:
				self.debug("Deleting old cache: " + name.decode('utf8', 'ignore'))
				del (cache[name])

		return False


	def _setCache(self, cache, name, ret_val):
		if len(ret_val) > 0:
			if not isinstance(cache, dict):
				cache = {}
			cache[name] = {"timestamp": time.time(),
						   "timeout": self.timeout,
						   "res": ret_val}
			self.debug("Saving cache: " + name + str(repr(cache[name]["res"]))[0:50])
			self.set("cache" + name, repr(cache))
		return ret_val


	def _connect(self):
		self._SocketInit()
		if self.platform == "win32" or xbmc.getCondVisibility('system.platform.android'):
			self.soccon = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.soccon = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		connected = False
		try:
			self.soccon.connect(self.socket)
			connected = True
		except socket.error, e:
			if e.errno in [111]:
				self.error("Service isn't running")
			else:
				self.error("Exception: " + repr(e) + " - " + repr(self.socket))
		return connected


	def debug(self, description):
		common.debug(description, "StorageServer")


	def info(self, description):
		common.info(description, "StorageServer")


	def warn(self, description):
		common.warn(description, "StorageServer")


	def error(self, description):
		common.error(description, "StorageServer")


	def run(self):
		self._SocketInit(True)
		if not self._StartDatabase():
			self._StartDatabase()
		if self.platform == "win32" or xbmc.getCondVisibility('system.platform.android'):
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			sock = socket.socket(socket.AF_UNIX)
		try:
			sock.bind(self.socket)
		except Exception, e:
			self.error("Exception: " + repr(e))
			self._ShowMessage(common.translate(100), common.translate(200))
			return False

		sock.listen(1)
		sock.setblocking(0)
		idle_since = time.time()
		waiting = 0
		while not self._Aborting():
			if waiting == 0:
				self.debug("Accepting connections")
				waiting = 1
			try:
				(self.clientsocket, address) = sock.accept()
				if waiting == 2:
					self.debug("Waking up, slept for %s seconds" % int(time.time() - idle_since))
				waiting = 0
			except socket.error, e:
				if e.errno == 11 or e.errno == 10035 or e.errno == 35:
					# There has to be a better way to accomplish this.
					if idle_since + self.idle < time.time():
						if self.instance:
							self.die = True
						if waiting == 1:
							self.debug("Idle for %s seconds, going to sleep" % self.idle)
						time.sleep(0.5)
						waiting = 2
					continue
				self.error("Exception: " + repr(e))
			except:
				pass

			if waiting:
				self.debug("Continue: " + repr(waiting))
				continue
			data = self._ReceiveData()
			self._RunCommand(data)
			idle_since = time.time()

		self.debug("Closing down")
		sock.close()
		if not self.platform == "win32" and not xbmc.getCondVisibility('system.platform.android'):
			if xbmcvfs.exists(self.socket):
				self.debug("Deleting socket file")
				xbmcvfs.delete(self.socket)


	def cacheFunction(self, funct=False, *args):
		self.debug("Function: " + repr(funct) + " - table name: " + repr(self.table))
		if funct and self.table:
			name = self._GenerateKey(funct, *args)
			cache = self.get("cache" + name)
			if cache.strip() == "":
				cache = {}
			else:
				cache = self._Evaluate(cache)
			ret_val = self._getCache(name, cache)
			if not ret_val:
				self.debug("Running: " + name.decode('utf8', 'ignore'))
				ret_val = funct(*args)
				self._setCache(cache, name, ret_val)
			if ret_val:
				self.debug("Returning result: " + str(len(ret_val)))
				return ret_val
			else:
				self.debug("Returning []. Got result: " + repr(ret_val))
				return []
		self.error("Error. Returning []")
		return []


	def cacheDelete(self, name):
		if self._connect() and self.table:
			temp = repr({"action": "del", "table": self.table, "name": "cache" + name})
			self._send(self.soccon, temp)
			res = self._recv(self.soccon)


	def cacheClean(self, empty=False):
		if self.table:
			cache = self.get("cache" + self.table)
			try:
				cache = self._Evaluate(cache)
			except:
				self.debug("Couldn't evaluate message : " + repr(cache))
			self.debug("Cache: " + repr(cache))
			if cache:
				new_cache = {}
				for item in cache:
					if (cache[item]["timestamp"] > time.time() - (3600)) and not empty:
						new_cache[item] = cache[item]
					else:
						self.debug("Deleting: " + item.decode('utf8', 'ignore'))
				self.set("cache", repr(new_cache))
				return True
		return False


	def lock(self, name):
		if self._connect() and self.table:
			data = repr({"action": "lock", "table": self.table, "name": name})
			self._send(self.soccon, data)
			res = self._recv(self.soccon)
			if res:
				res = self._Evaluate(res)
				if res == "true":
					return True
		return False


	def unlock(self, name):
		if self._connect() and self.table:
			data = repr({"action": "unlock", "table": self.table, "name": name})
			self._send(self.soccon, data)
			res = self._recv(self.soccon)
			if res:
				res = self._Evaluate(res)
				if res == "true":
					return True

		return False


	def setMulti(self, name, data):
		if self._connect() and self.table:
			temp = repr({"action": "set_multi", "table": self.table, "name": name, "data": data})
			res = self._send(self.soccon, temp)


	def getMulti(self, name, items):
		if self._connect() and self.table:
			self._send(self.soccon, repr({"action": "get_multi", "table": self.table, "name": name, "items": items}))
			res = self._recv(self.soccon)
			if res:
				res = self._Evaluate(res)
				if res == " ":  # We return " " as nothing.
					return ""
				else:
					return res
		return ""


	def delete(self, name):
		if self._connect() and self.table:
			temp = repr({"action": "del", "table": self.table, "name": name})
			self._send(self.soccon, temp)
			res = self._recv(self.soccon)


	def set(self, name, data):
		if self._connect() and self.table:
			temp = repr({"action": "set", "table": self.table, "name": name, "data": data})
			res = self._send(self.soccon, temp)


	def get(self, name):
		if self._connect() and self.table:
			self._send(self.soccon, repr({"action": "get", "table": self.table, "name": name}))
			res = self._recv(self.soccon)
			if res:
				res = self._Evaluate(res)
				return res.strip()  # We return " " as nothing. Strip it out.
		return ""


	def setCacheTimeout(self, timeout):
		self.timeout = float(timeout) * 3600


def RunAsync(func, *args, **kwargs):
	from threading import Thread

	worker = Thread(target=func, args=args, kwargs=kwargs)
	__workersByName[worker.getName()] = worker
	worker.start()
	return worker


def CheckInstanceMode():
	if xbmcaddon.Addon().getSetting("cache_autostart") == "false":
		s = StorageServer(table=False, instance=True)
		RunAsync(s.run)
		return True
	else:
		return False


CheckInstanceMode()