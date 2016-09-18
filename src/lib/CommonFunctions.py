# -*- coding: utf-8 -*-

import sys
import io
import re
import time
import urllib
import urllib2
import HTMLParser
import json


if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc
if hasattr(sys.modules["__main__"], "xbmcgui"):
	xbmcgui = sys.modules["__main__"].xbmcgui
else:
	import xbmcgui
if hasattr(sys.modules["__main__"], "xbmcaddon"):
	xbmcaddon = sys.modules["__main__"].xbmcaddon
else:
	import xbmcaddon
if hasattr(sys.modules["__main__"], "opener"):
	urllib2.install_opener(sys.modules["__main__"].opener)

USERAGENT = u"Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"


def log(txt, code="", level=0):
	if hasattr(sys.modules["__main__"], "__addonid__"):
		__addonid__ = sys.modules["__main__"]. __addonid__
	else:
		__addonid__ = xbmcaddon.Addon().getAddonInfo('id')
	if isinstance(txt, str):
		txt = txt.decode("utf-8")
	if not code:
		msgid = "%s" % __addonid__
	else:
		msgid = "%s [%s]" % (__addonid__, code)
	try:
		message = u"%s: %s" % (msgid, txt)
		xbmc.log(message.encode("utf-8"), level)
	except:
		message = u"%s: %s" % (msgid, repr(txt))
		xbmc.log(message.encode("utf-8"), level)


def debug(txt, code=""):
	log(txt, code, xbmc.LOGDEBUG)


def info(txt, code=""):
	log(txt, code, xbmc.LOGINFO)


def notice(txt, code=""):
	log(txt, code, xbmc.LOGNOTICE)


def warn(txt, code=""):
	log(txt, code, xbmc.LOGWARNING)


def error(txt, code=""):
	log(txt, code, xbmc.LOGERROR)


def translate(id):
	string = xbmcaddon.Addon().getLocalizedString(id).encode('utf-8', 'ignore')
	return string


def setting(id):
	return xbmcaddon.Addon().getSetting(id)


def PasswordDialog():
	if hasattr(sys.modules["__main__"], "__addonname__"):
		__addonname__ = sys.modules["__main__"]. __addonname__
	else:
		__addonname__ = xbmcaddon.Addon().getAddonInfo('name')
	pwd = ""
	keyboard = xbmc.Keyboard("", __addonname__ + ","  + translate(32016), True)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
		pwd = keyboard.getText()
	return pwd


def NotificationMsg(line, time=15000):
	if hasattr(sys.modules["__main__"], "__addonname__"):
		__addonname__ = sys.modules["__main__"]. __addonname__
	else:
		__addonname__ = xbmcaddon.Addon().getAddonInfo('name')
	if hasattr(sys.modules["__main__"], "__addonicon__"):
		__addonicon__ = sys.modules["__main__"]. __addonicon__
	else:
		__addonicon__ = xbmcaddon.Addon().getAddonInfo('icon')
	try:
		if isinstance(line, int):
			msg = translate(line)
		else:
			code = int(line)
			msg = translate(code)
	except:
		if not isinstance(line, int):
			msg = line
		else:
			msg = ""
	xbmc.executebuiltin("Notification(%s, %s, %d, %s)" %(__addonname__, msg, time, __addonicon__))


def AskRestart(msgid, s=0):
	if YesNoDialog(msgid):
		if s == 0:
			xbmc.executebuiltin("RestartApp")
		else:
			xbmc.executebuiltin("Reboot")


def YesNoDialog(line1="", line2="", line3=""):
	if hasattr(sys.modules["__main__"], "__addonname__"):
		__addonname__ = sys.modules["__main__"]. __addonname__
	else:
		__addonname__ = xbmcaddon.Addon().getAddonInfo('name')
	try:
		code = int(line1)
		msg1 = translate(code)
	except:
		msg1 = line1
	try:
		code = int(line2)
		msg2 = translate(code)
	except:
		msg2 = line2
	try:
		code = int(line3)
		msg3 = translate(code)
	except:
		msg3 = line3
	return xbmcgui.Dialog().yesno(__addonname__, line1=msg1, line2=msg2, line3=msg3)


def OkDialog(line1="", line2 = "", line3=""):
	if hasattr(sys.modules["__main__"], "__addonname__"):
		__addonname__ = sys.modules["__main__"]. __addonname__
	else:
		__addonname__ = xbmcaddon.Addon().getAddonInfo('name')
	try:
		code = int(line1)
		msg1 = translate(code)
	except:
		msg1 = line1
	try:
		code = int(line2)
		msg2 = translate(code)
	except:
		msg2 = line2
	try:
		code = int(line3)
		msg3 = translate(code)
	except:
		msg3 = line3
	return xbmcgui.Dialog().ok(__addonname__, line1=msg1, line2=msg2, line3=msg3)


# This function raises a keyboard for user input
def StringInputDialog(title=u"Input", default=u"", hidden=False):
	result = None
	# Fix for when this functions is called with default=None
	if not default:
		default = u""
	try:
		code = int(title)
		msg = translate(code)
	except:
		msg = title
	keyboard = xbmc.Keyboard(default, msg)
	keyboard.setHiddenInput(hidden)
	keyboard.doModal()
	if keyboard.isConfirmed():
		result = keyboard.getText()
	return result


# This function raises a keyboard numpad for user input
def NumberInputDialog(title=u"Input", default=u""):
	result = None
	# Fix for when this functions is called with default=None
	if not default:
		default = u""
	try:
		code = int(title)
		msg = translate(code)
	except:
		msg = title
	keyboard = xbmcgui.Dialog()
	result = keyboard.numeric(0, msg, default)
	return str(result)


# Converts the request url passed on by xbmc to the plugin into a dict of key-value pairs
def getParameters(parameterString):
	commands = {}
	parameterString = urllib.unquote_plus(parameterString)
	splitCommands = parameterString[parameterString.find('?') + 1:].split('&')
	for command in splitCommands:
		if (len(command) > 0):
			splitCommand = command.split('=')
			key = splitCommand[0]
			try:
				value = splitCommand[1].encode("utf-8")
			except:
				error("Error utf-8 encoding argument value: " + repr(splitCommand[1]), "CommonFunctions")
				value = splitCommand[1]
			commands[key] = value
	return commands


def replaceHTMLCodes(txt):
	# Fix missing ; in &#<number>;
	txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", makeUTF8(txt))
	txt = HTMLParser.HTMLParser().unescape(txt)
	txt = txt.replace("&amp;", "&")
	return txt


def stripTags(html):
	sub_start = html.find("<")
	sub_end = html.find(">")
	while sub_start < sub_end and sub_start > -1:
		html = html.replace(html[sub_start:sub_end + 1], "").strip()
		sub_start = html.find("<")
		sub_end = html.find(">")
	return html


def _getDOMContent(html, name, match, ret):  # Cleanup
	endstr = u"</" + name  # + ">"
	start = html.find(match)
	end = html.find(endstr, start)
	pos = html.find("<" + name, start + 1)
	while pos < end and pos != -1:  # Ignore too early </endstr> return
		tend = html.find(endstr, end + len(endstr))
		if tend != -1:
			end = tend
		pos = html.find("<" + name, pos + 1)
	if start == -1 and end == -1:
		result = u""
	elif start > -1 and end > -1:
		result = html[start + len(match):end]
	elif end > -1:
		result = html[:end]
	elif start > -1:
		result = html[start + len(match):]
	if ret:
		endstr = html[end:html.find(">", html.find(endstr)) + 1]
		result = match + result + endstr
	return result


def _getDOMAttributes(match, name, ret):
	lst = re.compile('<' + name + '.*?' + ret + '=([\'"].[^>]*?[\'"])>', re.M | re.S).findall(match)
	if len(lst) == 0:
		lst = re.compile('<' + name + '.*?' + ret + '=(.[^>]*?)>', re.M | re.S).findall(match)
	ret = []
	for tmp in lst:
		cont_char = tmp[0]
		if cont_char in "'\"":
			# Limit down to next variable.
			if tmp.find('=' + cont_char, tmp.find(cont_char, 1)) > -1:
				tmp = tmp[:tmp.find('=' + cont_char, tmp.find(cont_char, 1))]
			# Limit to the last quotation mark
			if tmp.rfind(cont_char, 1) > -1:
				tmp = tmp[1:tmp.rfind(cont_char)]
		else:
			if tmp.find(" ") > 0:
				tmp = tmp[:tmp.find(" ")]
			elif tmp.find("/") > 0:
				tmp = tmp[:tmp.find("/")]
			elif tmp.find(">") > 0:
				tmp = tmp[:tmp.find(">")]
		ret.append(tmp.strip())
	return ret


def _getDOMElements(item, name, attrs):
	lst = []
	for key in attrs:
		lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=[\'"]' + attrs[key] + '[\'"].*?>))', re.M | re.S).findall(item)
		if len(lst2) == 0 and attrs[key].find(" ") == -1:  # Try matching without quotation marks
			lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=' + attrs[key] + '.*?>))', re.M | re.S).findall(item)

		if len(lst) == 0:
			debug("Setting main list " + repr(lst2), "CommonFunctions")
			lst = lst2
			lst2 = []
		else:
			debug("Setting new list " + repr(lst2), "CommonFunctions")
			test = range(len(lst))
			test.reverse()
			for i in test:  # Delete anything missing from the next list.
				if not lst[i] in lst2:
					debug("Purging mismatch " + str(len(lst)) + " - " + repr(lst[i]), "CommonFunctions")
					del (lst[i])

	if len(lst) == 0 and attrs == {}:
		debug("No list found, trying to match on name only", "CommonFunctions")
		lst = re.compile('(<' + name + '>)', re.M | re.S).findall(item)
		if len(lst) == 0:
			lst = re.compile('(<' + name + ' .*?>)', re.M | re.S).findall(item)
	return lst


def parseDOM(html, name=u"", attrs={}, ret=False):
	if isinstance(name, str): # Should be handled
		try:
			name = name #.decode("utf-8")
		except:
			debug("Couldn't decode name binary string: " + repr(name), "CommonFunctions")
	if isinstance(html, str):
		try:
			html = [html.decode("utf-8")] # Replace with chardet thingy
		except:
			debug("Couldn't decode html binary string. Data length: " + repr(len(html)), "CommonFunctions")
			html = [html]
	elif isinstance(html, unicode):
		html = [html]
	elif not isinstance(html, list):
		debug("Input isn't list or string/unicode", "CommonFunctions")
		return u""
	if not name.strip():
		debug("Missing tag name", "CommonFunctions")
		return u""

	ret_lst = []
	for item in html:
		temp_item = re.compile('(<[^>]*?\n[^>]*?>)').findall(item)
		for match in temp_item:
			item = item.replace(match, match.replace("\n", " "))
		lst = _getDOMElements(item, name, attrs)
		if isinstance(ret, str):
			debug("Getting attribute %s content for %s matches " % (ret, len(lst) ), "CommonFunctions")
			lst2 = []
			for match in lst:
				lst2 += _getDOMAttributes(match, name, ret)
			lst = lst2
		else:
			debug("Getting element content for %s matches " % len(lst), "CommonFunctions")
			lst2 = []
			for match in lst:
				debug("Getting element content for %s" % match, "CommonFunctions")
				temp = _getDOMContent(item, name, match, ret).strip()
				item = item[item.find(temp, item.find(match)) + len(temp):]
				lst2.append(temp)
			lst = lst2
		ret_lst += lst
	return ret_lst


def extractJS(data, function=False, variable=False, match=False, evaluate=False, values=False):
	scripts = parseDOM(data, "script")
	if len(scripts) == 0:
		debug("Couldn't find any script tags. Assuming javascript file was given", "CommonFunctions")
		scripts = [data]
	lst = []
	for script in scripts:
		tmp_lst = []
		if function:
			tmp_lst = re.compile(function + '\(.*?\).*?;', re.M | re.S).findall(script)
		elif variable:
			tmp_lst = re.compile(variable + '[ ]+=.*?;', re.M | re.S).findall(script)
		else:
			tmp_lst = [script]
		if len(tmp_lst) > 0:
			debug("Found: " + repr(tmp_lst), "CommonFunctions")
			lst += tmp_lst
		else:
			debug("Found nothing on: " + script, "CommonFunctions")

	test = range(0, len(lst))
	test.reverse()
	for i in test:
		if match and lst[i].find(match) == -1:
			debug("Removing item: " + repr(lst[i]), "CommonFunctions")
			del lst[i]
		else:
			debug("Cleaning item: " + repr(lst[i]), "CommonFunctions")
			if lst[i][0] == u"\n":
				lst[i] == lst[i][1:]
			if lst[i][len(lst) - 1] == u"\n":
				lst[i] == lst[i][:len(lst) - 2]
			lst[i] = lst[i].strip()

	if values or evaluate:
		for i in range(0, len(lst)):
			debug("Getting values %s" % lst[i], "CommonFunctions")
			if function:
				if evaluate: # include the ( ) for evaluation
					data = re.compile("(\(.*?\))", re.M | re.S).findall(lst[i])
				else:
					data = re.compile("\((.*?)\)", re.M | re.S).findall(lst[i])
			elif variable:
				tlst = re.compile(variable + ".*?=.*?;", re.M | re.S).findall(lst[i])
				data = []
				for tmp in tlst: # This breaks for some stuff. "ad_tag": "http://ad-emea.doubleclick.net/N4061/pfadx/com.ytpwatch.entertainment/main_563326'' # ends early, must end with }
					cont_char = tmp[0]
					cont_char = tmp[tmp.find("=") + 1:].strip()
					cont_char = cont_char[0]
					if cont_char in "'\"":
						debug("Using %s as quotation mark" % cont_char, "CommonFunctions")
						tmp = tmp[tmp.find(cont_char) + 1:tmp.rfind(cont_char)]
					else:
						debug("No quotation mark found", "CommonFunctions")
						tmp = tmp[tmp.find("=") + 1: tmp.rfind(";")]
					tmp = tmp.strip()
					if len(tmp) > 0:
						data.append(tmp)
			else:
				error("Don't know what to extract values from", "CommonFunctions")

			debug("Values extracted: %s" % repr(data), "CommonFunctions")
			if len(data) > 0:
				lst[i] = data[0]

	if evaluate:
		for i in range(0, len(lst)):
			debug("Evaluating %s" % lst[i], "CommonFunctions")
			data = lst[i].strip()
			try:
				try:
					lst[i] = json.loads(data)
				except:
					notice("Couldn't json.loads, trying eval", "CommonFunctions")
					lst[i] = eval(data)
			except:
				error("Couldn't eval: %s from %s" % (repr(data), repr(lst[i])), "CommonFunctions")
	return lst


def fetchPage(params={}):
	get = params.get
	link = get("link")
	ret_obj = {}

	if get("post_data"):
		debug("Called for: " + repr(params['link']), "CommonFunctions")
	else:
		debug("Called for: " + repr(params), "CommonFunctions")
	if not link or int(get("error", "0")) > 2:
		debug("Giving up")
		ret_obj["status"] = 500
		return ret_obj
	if get("post_data"):
		if get("hide_post_data"):
			debug("Posting data", "CommonFunctions")
		else:
			debug("Posting data: " + urllib.urlencode(get("post_data")), "CommonFunctions")
		request = urllib2.Request(link, urllib.urlencode(get("post_data")))
		request.add_header('Content-Type', 'application/x-www-form-urlencoded')
	else:
		debug("Got request", "CommonFunctions")
		request = urllib2.Request(link)
	if get("headers"):
		for head in get("headers"):
			request.add_header(head[0], head[1])
	request.add_header('User-Agent', USERAGENT)
	if get("cookie"):
		request.add_header('Cookie', get("cookie"))
	if get("refering"):
		request.add_header('Referer', get("refering"))

	try:
		debug("Connecting to server..", "CommonFunctions")
		con = urllib2.urlopen(request)
		ret_obj["header"] = con.info()
		ret_obj["new_url"] = con.geturl()
		if get("no-content", "false") == u"false" or get("no-content", "false") == "false":
			inputdata = con.read()
			ret_obj["content"] = inputdata.decode("utf-8")
		con.close()
		ret_obj["status"] = 200
		return ret_obj
	except urllib2.HTTPError, e:
		err = str(e)
		debug("HTTP Error: " + err + ". Headers: " + str(e.headers) + ". Content: " + e.fp.read(), "CommonFunctions")
		params["error"] = str(int(get("error", "0")) + 1)
		ret = fetchPage(params)
		if not "content" in ret and e.fp:
			ret["content"] = e.fp.read()
			return ret
		ret_obj["status"] = 500
		return ret_obj
	except urllib2.URLError, e:
		err = str(e)
		debug("URL Error: " + err, "CommonFunctions")
		time.sleep(3)
		params["error"] = str(int(get("error", "0")) + 1)
		ret_obj = fetchPage(params)
		return ret_obj


def getCookieInfoAsHTML():
	if hasattr(sys.modules["__main__"], "cookiejar"):
		cookiejar = sys.modules["__main__"].cookiejar
		cookie = repr(cookiejar)
		cookie = cookie.replace("<_LWPCookieJar.LWPCookieJar[", "")
		cookie = cookie.replace("), Cookie(version=0,", "></cookie><cookie ")
		cookie = cookie.replace(")]>", "></cookie>")
		cookie = cookie.replace("Cookie(version=0,", "<cookie ")
		cookie = cookie.replace(", ", " ")
		debug("Cookie: %s" % repr(cookie), "CommonFunctions")
		return cookie
	debug("Found no cookie", "CommonFunctions")
	return ""


# This function implements a horrible hack related to python 2.4's terrible unicode handling.
def makeAscii(data):
	try:
		return data.encode('ascii', "ignore")
	except:
		debug("Hit exception during encoding: " + repr(data), "CommonFunctions")
		s = u""
		for i in data:
			try:
				i.encode("ascii", "ignore")
			except:
				debug("Can't encode character: %s" % i)
				continue
			else:
				s += i
		return s


# This function handles stupid utf handling in python.
def makeUTF8(data):
	try:
		return data.decode('utf8', 'xmlcharrefreplace') # was 'ignore'
	except:
		debug("Hit exception during decoding on: " + repr(data), "CommonFunctions")
		s = u""
		for i in data:
			try:
				i.decode("utf8", "xmlcharrefreplace")
			except:
				debug("Can't decode character: %s" % i, "CommonFunctions")
				continue
			else:
				s += i
		return s


def openFile(filepath, options=u"r"):
	if options.find("b") == -1:  # Toggle binary mode on failure
		alternate = options + u"b"
	else:
		alternate = options.replace(u"b", u"")

	try:
		debug("Trying normal: %s" % options, "CommonFunctions")
		return io.open(filepath, options)
	except:
		debug("Fallback to binary: %s" % alternate, "CommonFunctions")
		return io.open(filepath, alternate)
