# -*- coding: utf-8 -*-

import os
import abc
import sys
import common

if hasattr(sys.modules["__main__"], "xbmcgui"):
	xbmcgui = sys.modules["__main__"].xbmcgui
else:
	import xbmcgui



class ServiceRunner(object):
	__metaclass__ = abc.ABCMeta
	HOME = os.environ['HOME']
	CONFIG_CACHE = os.environ.get('CONFIG_CACHE', '%s/.cache' % HOME)
	USER_CONFIG = os.environ.get('USER_CONFIG', '%s/.config' % HOME)


	def __init__(self):
		pass


	def __repr__(self):
		return str(self.__class__) + " (" + str(self.code()) + ")"


	@abc.abstractmethod
	def code(self):
		return None
		pass


	@abc.abstractmethod
	def run(self, *arg):
		pass


	def debug(self, txt):
		common.debug(txt, "runner")


	def info(self, txt):
		common.info(txt, "runner")


	def notice(self, txt):
		common.notice(txt, "runner")


	def warn(self, txt):
		common.warn(txt, "runner")


	def error(self, txt):
		common.error(txt, "runner")

	@property
	def windowid(self):
		try:
			id = xbmcgui.getCurrentWindowDialogId()
		except:
			id = None
		if id is not None and id != '' and id != 0:
			self.debug("Detected current dialog window id: %s " %str(id))
			return id
		else:
			try:
				id = xbmcgui.getCurrentWindowId()
			except:
				id = None
			if id is not None and id != '' and id != 0:
				self.debug("Detected current dialog window id: %s " % str(id))
				return id
			else:
				return None


	def window(self, id=None):
		if id is None:
			id = self.windowid
		if id is not None:
			try:
				window = xbmcgui.WindowDialog(int(id))
			except:
				window = None
			if window is not None:
				self.debug("Detected dialog window object: %s " % str(window))
				return window
			else:
				try:
					window = xbmcgui.Window(int(id))
				except:
					window = None
				if window is not None:
					self.debug("Detected window object: %s " % str(window))
					return window
				else:
					return None


	def _function(self, cmd, *args, **kwargs):
		if cmd is not None and cmd != '':
			if str(cmd).find('.') > 0:
				if str(cmd).startswith("self."):
					cmd = str(cmd).split(".")[1]
					return common.clscall(self, cmd, *args, **kwargs)
				else:
					cls = str(cmd).split(".")[0]
					cmd = str(cmd).split(".")[1]
					return common.clscall(cls, cmd, *args, **kwargs)
			else:
				return common.funcall(cmd, *args, **kwargs)
		else:
			return None


	def _process(self, cmd):
		if cmd is not None and cmd != '':
			return common.procexec(cmd)
		else:
			return None


	def any2int(self, v, error=False, none=True):
		return common.any2int(v, error=error,none=none)


	def any2float(self, v, error=False, none=True):
		return common.any2float(v, error=error,none=none)


	def any2str(self, v, error=False, none=True):
		return common.any2str(v, error=error,none=none)


	# Function: str2bool
	def any2bool(self, v, error=False, none=True):
		return common.any2bool(v, error=error,none=none)


	@property
	def addon(self):
		return common.Addon()


	def translate(self, code):
		return common.translate(code)


	def getExControl(self, control, mix=0):
		"""Get control instance for any part for group"""
		if control is not None:
			if isinstance(control, int):
				control = self.window().getControl(control)
			elif isinstance(control, str):
				control = self.window().getControl(int(control))
			if mix > 0:
				control = self.window().getControl(10 * control.getId() + mix)
			return control
		else:
			raise RuntimeError('Invalid control reference')


	def setControlLabel(self, control, label):
		"""Set label control"""
		if control is not None:
			# get control instance
			if isinstance(control, int):
				control = self.getExControl(control)
			elif isinstance(control, str):
				control = self.getExControl(int(control))
			# take translated label
			if isinstance(label, int) :
				label = self.translate(label)
			# set label
			if isinstance(control, xbmcgui.Control):
				control.setLabel(str(label))


	def getControlValue(self, control):
		value = None
		if control is not None:
			# get control instance
			if isinstance(control, int):
				control = self.getExControl(control)
			elif isinstance(control, str):
				control = self.getExControl(int(control))
			# get control value
			if isinstance(control, xbmcgui.ControlButton):
				value = control.getLabel()
			else:
				value = control.getText()
			# adapt value
			if value is None:
				value = ""
		return value


	def setControlValue(self, control, data, key=None):
		value = None
		if control is not None:
			# get control instance
			if isinstance(control, int):
				control = self.getExControl(control)
			elif isinstance(control, str):
				control = self.getExControl(int(control))
			# set value from dictionary using specified key name
			if data is not None and isinstance(data, dict) and key is not None and key != '':
				if key in data:
					value = data[key]
			# set value from list using specified key index
			elif data is not None and isinstance(data, list) and key is not None and isinstance(key, int):
				if int(key) < len(data):
					value = data[key]
			# set value based on the specified type and content
			elif (isinstance(data, str) or isinstance(data, int) or isinstance(data, float)) and key is None:
				value = str(data)
			# adapt value
			if value is None:
				value = ""
			if isinstance(control, xbmcgui.ControlButton):
				control.setLabel(value)
			else:
				control.setText(value)


	def setControlStatus(self, control, data, key=None, value=None):
		if control is not None:
			if isinstance(control, int):
				control = self.getExControl(control)
			elif isinstance(control, str):
				control = self.getExControl(int(control))
			if isinstance(data, dict) and data is not None and key is not None and key != '':
				dataval = None
				if key in data:
					dataval = data[str(key)]
				if isinstance(value, list):
					control.setEnabled(dataval in value)
				else:
					control.setEnabled(dataval == value)
			elif isinstance(data, list) and data is not None and isinstance(key, int) and key is not None:
				dataval = None
				if int(key) < len(data):
					dataval = data[int(key)]
				if isinstance(value, list):
					control.setEnabled(dataval in value)
				else:
					control.setEnabled(dataval == value)
			elif (isinstance(data, str) or isinstance(data, int) or isinstance(data, float)) and key is None and value is not None:
				if isinstance(value, list):
					control.setEnabled(data in value)
				else:
					control.setEnabled(data == value)
			elif isinstance(data, bool):
				control.setEnabled(data)
			elif data is None:
				control.setEnabled(False)


	def setControlSelection(self, control, data, key=None, value=None):
		if control is not None:
			if isinstance(control, int):
				control = self.getExControl(control)
			elif isinstance(control, str):
				control = self.getExControl(int(control))
			if isinstance(data, dict) and data is not None and key is not None and key != '':
				dataval = None
				if key in data:
					dataval = data[str(key)]
				if isinstance(value, list):
					control.setSelected(dataval in value)
				else:
					control.setSelected(dataval == value)
			elif isinstance(data, list) and data is not None and isinstance(key, int) and key is not None:
				dataval = None
				if int(key) < len(data):
					dataval = data[int(key)]
				if isinstance(value, list):
					control.setSelected(dataval in value)
				else:
					control.setSelected(dataval == value)
			elif (isinstance(data, str) or isinstance(data, int) or isinstance(data, float)) and key is None and value is not None:
				if isinstance(value, list):
					control.setSelected(data in value)
				else:
					control.setSelected(data == value)
			elif isinstance(data, bool):
				control.setSelected(data)
			elif data is None:
				control.setSelected(False)


	def getControlSelection(self, control):
		if control is not None:
			if isinstance(control, int):
				control = self.getExControl(control)
			elif isinstance(control, str):
				control = self.getExControl(int(control))
			return control.isSelected()
		else:
			return None


	def setControlValueOnClick(self, control, type=0, message=''):
		_output = None
		_input = self.getControlValue(control)
		if isinstance(message, int):
			message = self.translate(message)
		if isinstance(type, int):
			if type == 0:
				keyboard = self.getTextPadKeyboard(_input, message, False)
				keyboard.doModal()
				if keyboard.isConfirmed():
					_output = keyboard.getText()
			elif type == 1:
				_output = self.getNumPadKeyboard(_input, message)
			elif type == 2:
				_output = self.getIPAddrPadKeyboard(_input, message)
			elif type == 3:
				_output = self.getDatePadKeyboard(_input, message)
			elif type == 4:
				_output = self.getTimePadKeyboard(_input, message)
		if isinstance(type, list):
			_output = self.getSelectDialog(message, type)
		if _output != _input:
			self.setControlValue(control, _output)
			return True
		else:
			return False


	def newListItem(self, label, label2=None):
		if label is not None and isinstance(label, int):
			label = self.translate(label)
		if label2 is not None and isinstance(label2, int):
			label2 = self.translate(label2)
		item = xbmcgui.ListItem()
		if label is not None:
			item.setLabel(label)
		if label2 is not None:
			item.setLabel2(label2)
		return item


	def getOkDialog(self, txt):
		return xbmcgui.Dialog().ok(self.addon.getAddonInfo('name'), txt)


	def getSelectDialog(self, title, options):
		_answer = None
		if options is not None and len(options) > 0:
			_index = xbmcgui.Dialog().select(title, options)
			if -1 < _index < len(options):
				_answer = options[_index]
		return _answer


	def input(self, *args):
		params = {}
		if len(args) > 1:
			for i in args:
				arg = i
				if arg.startswith('?'):
					arg = arg[1:]
				params.update(dict(common.urlparsequery(arg)))
		return params
