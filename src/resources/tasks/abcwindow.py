# -*- coding: utf-8 -*-

import abc
import sys
import common
from .abcservice import ServiceTask

if hasattr(sys.modules["__main__"], "xbmcgui"):
	xbmcgui = sys.modules["__main__"].xbmcgui
else:
	import xbmcgui


class WindowTask(ServiceTask, xbmcgui.WindowXMLDialog):
	__metaclass__ = abc.ABCMeta
	key = "window"


	def __init__(self, *args, **kwargs):
		ServiceTask.__init__(self)
		xbmcgui.WindowXMLDialog.__init__(self, *args, **kwargs)
		self._wait = None


	def load(self):
		pass


	def dispose(self):
		self.clearProperties()
		self.close()


	def start(self, *args):
		pass


	def run(self, *args):
		self.start(args)
		self.show()


	def show(self):
		self.doModal()


	def onInit(self):
		self._lock()
		self.load()
		self._unlock()


	def onClick(self, id):
		_method = "onClick_%s" %str(id)
		if hasattr(self, _method):
			self.debug("Calling method: %s.%s" %( self.__class__.__name__,str(_method)))
			self._function(".".join(["self", _method]))


	def onFocus(self, id):
		_method = "onFocus_%s" %str(id)
		if hasattr(self, _method):
			self.debug("Calling method: %s.%s" %( self.__class__.__name__,str(_method)))
			self._function(".".join(["self", _method]))


	@property
	def addon(self):
		return common.Addon()


	def _lock(self, txt=None):
		"""
		Lock the screen until execution of a backend command
		:param txt: text message to be displayed
		"""
		if self._wait is None:
			self._wait = xbmcgui.WindowXMLDialog("WaitDialog.xml", self.addon.getAddonInfo('path'))
			self._wait.show()
		if self._wait is not None and txt is not None:
			self._wait.getExControl(1000).setLabel(txt)
			self._wait.getExControl(1000).setVisible(True)


	def _unlock(self):
		"""
		Unlocking the screen; should be executed once the backend command is finished
		"""
		if self._wait is not None:
			self._wait.close()
			self._wait = None


	def set(self, id, value):
		self.setProperty("Value.%s" %str(id), value)


	def get(self, id):
		return self.getProperty("Value.%s" %str(id))


	def getExControl(self, control, mix=0):
		"""Get control instance for any part for group"""
		if control is not None:
			if isinstance(control, int):
				control = self.getControl(control)
			elif isinstance(control, str):
				control = self.getControl(int(control))
			if mix > 0:
				control = self.getControl(10 * control.getId() + mix)
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
				keyboard = common.StringInputDialog(_input, message, False)
				keyboard.doModal()
				if keyboard.isConfirmed():
					_output = keyboard.getText()
			elif type == 1:
				_output = common.NumberInputDialog(_input, message)
			elif type == 2:
				_output = common.IPAddrInputDialog(_input, message)
			elif type == 3:
				_output = common.DateInputDialog(_input, message)
			elif type == 4:
				_output = common.TimeInputDialog(_input, message)
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

