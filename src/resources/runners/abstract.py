# -*- coding: utf-8 -*-

import abc



class ServiceRunner(object):
	__metaclass__ = abc.ABCMeta


	def __repr__(self):
		return str(self.__class__) + " (" + str(self.code()) + ")"


	@abc.abstractmethod
	def code(self):
		return None
		pass


	@abc.abstractmethod
	def run(self, *arg):
		pass


	def input(self, *args):
		params = {}
		if len(args) > 1:
			for i in args:
				arg = i
				if arg.startswith('?'):
					arg = arg[1:]
				params.update(dict(parse_qsl(arg)))
		return params


def parse_qsl(qs, keep_blank_values=0, strict_parsing=0, max_num_fields=None):
	"""Parse a query given as a string argument.
	Arguments:
	qs: percent-encoded query string to be parsed
	keep_blank_values: flag indicating whether blank values in
		percent-encoded queries should be treated as blank strings.  A
		true value indicates that blanks should be retained as blank
		strings.  The default false value indicates that blank values
		are to be ignored and treated as if they were  not included.
	strict_parsing: flag indicating what to do with parsing errors. If
		false (the default), errors are silently ignored. If true,
		errors raise a ValueError exception.
	max_num_fields: int. If set, then throws a ValueError if there
		are more than n fields read by parse_qsl().
	Returns a list, as G-d intended.
	"""
	# If max_num_fields is defined then check that the number of fields
	# is less than max_num_fields. This prevents a memory exhaustion DOS
	# attack via post bodies with many fields.
	if max_num_fields is not None:
		num_fields = 1 + qs.count('&') + qs.count(';')
		if max_num_fields < num_fields:
			raise ValueError('Max number of fields exceeded')
	pairs = [s2 for s1 in qs.split('&') for s2 in s1.split(';')]
	r = []
	for name_value in pairs:
		if not name_value and not strict_parsing:
			continue
		nv = name_value.split('=', 1)
		if len(nv) != 2:
			if strict_parsing:
				raise ValueError("Bad query field: %r" % (name_value,))
			# Handle case of a control-name with no equal sign
			if keep_blank_values:
				nv.append('')
			else:
				continue
		if len(nv[1]) or keep_blank_values:
			name = unquote(str(nv[0]).replace('+', ' '))
			value = unquote(str(nv[1]).replace('+', ' '))
			r.append((name, value))
	return r

_hexdig = '0123456789ABCDEFabcdef'
_hextochr = dict((a+b, chr(int(a+b,16)))
				for a in _hexdig for b in _hexdig)

def unquote(s):
	"""unquote('abc%20def') -> 'abc def'."""
	bits = s.split('%')
	# fastpath
	if len(bits) == 1:
		return s
	res = [bits[0]]
	append = res.append
	for item in bits[1:]:
		try:
			append(_hextochr[item[:2]])
			append(item[2:])
		except KeyError:
			append('%')
			append(item)
	return ''.join(res)
