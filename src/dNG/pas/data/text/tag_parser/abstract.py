# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.tag_parser.Abstract
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;tag_parser

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasTagParserVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

import re

from dNG.pas.runtime.not_implemented_exception import NotImplementedException

class Abstract(object):
#
	"""
The abstract parser implements methods to find and process "[tags]".

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: tag_parser
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Abstract)

:since: v0.1.00
		"""

		self.log_handler = None
		"""
The LogHandler is called whenever debug messages should be logged or errors
happened.
		"""
	#

	def _find_end_tag_position(self, data, data_position, tag_end):
	#
		"""
Find the starting position of the closing tag.

:param data: String that contains convertable data
:param data_position: Current parser position
:param tag_end: Tag end definition

:return: (int) Position; -1 if not found
:since:  v0.1.00
		"""

		_return = None

		is_valid = True
		result = -1

		while ((_return == None or _return > -1) and is_valid):
		#
			result = data.find(tag_end, data_position)
			if (result > -1 and (_return == None or result < _return)): _return = result

			if (_return == None): _return = -1
			elif (_return > -1):
			#
				data_position = _return
				if (data[_return - 1:_return] != "\\"): is_valid = False
			#
		#

		return _return
	#

	def _find_tag_end_position(self, data, data_position):
	#
		"""
Find the starting position of the enclosing content.

:param data: String that contains convertable data
:param data_position: Current parser position

:return: (int) Position; -1 if not found
:since:  v0.1.00
		"""

		_return = None

		is_valid = True

		while ((_return == None or _return > -1) and is_valid):
		#
			_return = data.find("]", data_position)

			if (_return > -1):
			#
				data_position = _return
				if (data[_return - 1:_return] != "\\"): is_valid = False
			#
		#

		if (_return > -1): _return += 1
		return _return
	#

	def _match_change(self, tag_definition, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the matched tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.00
		"""

		raise NotImplementedException()
	#

	def _match_check(self, data):
	#
		"""
Check if a possible tag match is a false positive.

:param data: Data starting with the possible tag

:return: (dict) Matched tag definition; None if false positive
:since:  v0.1.00
		"""

		return None
	#

	def _parse(self, data, data_position = 0, nested_tag_end_position = None):
	#
		"""
Parse for "[tags]" and calls "_match_check()" for possible hits.

:param data: Data to be parsed
:param data_position: Current parser position
:param nested_tag_end_position: End position for nested tags

:return: (bool) True if replacements happened
:since:  v0.1.00
		"""

		if (nested_tag_end_position == None):
		#
			data_position = data.find("[", data_position)
			nested_check = False
		#
		else:
		#
			data_position = data.find("[", data_position)
			if (data_position >= nested_tag_end_position): data_position = -1

			nested_check = True
			tag_end_position = -1
		#

		while (data_position > -1):
		#
			tag_definition = self._match_check(data[data_position:])

			if (tag_definition == None): data_position += 1
			else:
			#
				is_simple_tag = ("type" in tag_definition and tag_definition['type'] == "simple")
				is_valid = False
				tag_length = len(tag_definition['tag'])

				tag_element_end_position = self._find_tag_end_position(data, data_position + 1 + tag_length)
				tag_end_position = -1

				if (is_simple_tag): is_valid = (tag_element_end_position > -1)
				elif (tag_element_end_position > -1):
				#
					tag_end_position = self._find_end_tag_position(data, tag_element_end_position, tag_definition['tag_end'])

					if (tag_end_position >= 0):
					#
						( data, tag_end_position ) = (
							self._parse_nested_walker(data, data_position, tag_definition, tag_end_position)
							if ("type" not in tag_definition or tag_definition['type'] != "top_down") else
							self._parse_top_down_walker(data, data_position, tag_definition, tag_end_position)
						)

						is_valid = (tag_end_position > -1)
					#
				#

				if (is_valid):
				#
					if (self.log_handler != None): self.log_handler.debug("{0!r} found '{1}' at {2:d}".format(self, tag_definition['tag'], data_position))
					data = self._match_change(tag_definition, data, data_position, tag_element_end_position, tag_end_position)
				#
				else: data_position += tag_length
			#

			if (nested_check): data_position = -1
			else: data_position = data.find("[", data_position)
		#

		if (nested_check and tag_end_position < 0): data = None
		return data
	#

	def _parse_nested_walker(self, data, data_position, tag_definition, tag_end_position):
	#
		"""
Parse nested tags recursively.

:param data: Data to be parsed
:param data_position: Current parser position
:param tag_definition: Matched tag definition
:param tag_end_position: Starting position of the closing tag

:return: (int) New starting position of the closing tag
:since:  v0.1.00
		"""

		_return = tag_end_position

		nested_data = self._parse(data, data_position + 1, tag_end_position)

		while (nested_data != None):
		#
			data = nested_data
			tag_element_end_position = self._find_tag_end_position(data, data_position + 1)
			if (tag_element_end_position > -1): _return = self._find_end_tag_position(data, tag_element_end_position, tag_definition['tag_end'])

			nested_data = self._parse(data, data_position + 1, _return)
		#

		return ( data, _return )
	#

	def _parse_top_down_walker(self, data, data_position, tag_definition, tag_end_position):
	#
		"""
Parse nested tags of the same type to find the correct end position.

:param data: Data to be parsed
:param data_position: Current parser position
:param tag_definition: Matched tag definition
:param tag_end_position: Starting position of the closing tag

:return: (int) New starting position of the closing tag
:since:  v0.1.00
		"""

		_return = tag_end_position

		tag_length = len(tag_definition['tag'])

		nested_tag_position = data.find("[" + tag_definition['tag'], data_position + 1 + tag_length)
		tag_end_length = len(tag_definition['tag_end'])

		while (nested_tag_position >= 0 and nested_tag_position < _return):
		#
			if (self._match_check(data[nested_tag_position:]) != None): _return = self._find_end_tag_position(data, _return + tag_end_length, tag_definition['tag_end'])
			nested_tag_position = data.find("[" + tag_definition['tag'], nested_tag_position + 1 + tag_length)
		#

		return ( data, _return )
	#

	@staticmethod
	def parse_tag_parameters(tag_key, data, tag_position, data_position):
	#
		"""
Check if a possible tag matches the given expected, simple tag.

:param tag_key: Tag key
:param data: Data starting with the possible tag
:param tag_position: Tag starting position
:param data_position: Data starting position

:return: (bool) True if valid
:since:  v0.1.01
		"""

		_return = { }

		data_splitted = data[1 + len(tag_key) + tag_position:data_position - 1].split(":", 1)

		data = (data_splitted[0] if (len(data_splitted[0]) > 0 or len(data_splitted) > 1) else None)
		re_escaped = re.compile("(\\\\+)$")
		value = ""

		while (data != None):
		#
			if (len(data) > 0):
			#
				re_result = re_escaped.search(data)
				value += data

				if (re_result == None or (len(re_result.group(1)) % 2) != 1):
				#
					value_splitted = value.split("=", 1)

					if (len(value_splitted) > 1):
					#
						key = value_splitted[0]
						value = value_splitted[1]
					#
					else: key = tag_key

					if (key not in _return): _return[key] = value
					value = ""
				#
			#

			if (len(data_splitted) > 1):
			#
				data_splitted = data_splitted[1].split(":", 1)
				data = data_splitted[0]
			#
			else: data = None
		#

		return _return
	#
#

##j## EOF