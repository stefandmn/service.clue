# -*- coding: utf-8 -*-

__all__ = ['run']

import platform
import traceback
import Commons as commons
from mediadir.impl.ClueRunner import ClueRunner as Runner
from mediadir.impl.ClueContext import ClueContext as Context


def run(provider, context=None):
	try:
		if not context:
			context = Context()
		runner = Runner()
		context.debug('Starting Media Directory framework...')
		py_version = 'Python %s' % str(platform.python_version())
		cx_version = context.getSystemVersion()
		context.notice('Starting %s (%s) on %s with %s' % (context.getName(), context.getVersion(), cx_version, py_version))
		context.debug('Execution details: path = %s, parameters = %s' %(context.getPath(), unicode(context.getParams())))
		# Run provider
		runner.run(provider, context)
		context.debug('Shutdown of Media Directory framework')
	except BaseException as bex:
		traceback.print_exc()
		commons.error("Error executing Media Directory framework: " + str(bex))
		if context is not None:
			context.getUI().closeBusyDialog()
			context.getUI().onOk(context.getName(), "Error running Media Directory framework: " + str(bex))
		else:
			commons.OkDialog("Error running Media Directory framework: " + str(bex))
	pass
