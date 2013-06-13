# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.tag_parser.Abstract
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
The log_handler is called whenever debug messages should be logged or errors
happened.
		"""
	#

	def __del__(self):
	#
		"""
Destructor __del__(Abstract)

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.return_instance()
	#

	def parser(self, data, data_position = 0, nested_tag_end_position = None):
	#
		"""
Parse for "[tags]" and calls "parser_check()" for possible hits.

:param data: Data to be parsed
:param data_position: Current parser position
:param nested_tag_end_position: End position for nested tags 

:access: protected
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
			tag_definition = self.parser_check(data[data_position:])

			if (tag_definition == None): data_position += 1
			else:
			#
				tag_length = len(tag_definition['tag'])
				tag_start_end_position = self.parser_tag_find_end_position(data, data_position + 1 + tag_length)
				tag_end_position = -1

				if (tag_start_end_position > -1):
				#
					tag_end_position = self.parser_tag_end_find_position(data, tag_start_end_position, tag_definition['tag_end'])

					if (tag_end_position >= 0):
					#
						if ("type" not in tag_definition or tag_definition['type'] != "top_down"):
						#
							nested_data = self.parser(data, data_position + 1, tag_end_position)

							while (nested_data != None):
							#
								data = nested_data
								tag_start_end_position = self.parser_tag_find_end_position(data, data_position + 1)
								if (tag_start_end_position > -1): tag_end_position = self.parser_tag_end_find_position(data, tag_start_end_position, tag_definition['tag_end'])

								nested_data = self.parser(data, data_position + 1, tag_end_position)
							#
						#
						else:
						#
							nested_tag_position = data.find("[" + tag_definition['tag'], data_position + 1 + tag_length)
							tag_end_length = len(tag_definition['tag_end'])

							while (nested_tag_position >= 0 and nested_tag_position < tag_end_position):
							#
								if (self.parser_check(data[nested_tag_position:]) != None): tag_end_position = self.parser_tag_end_find_position(data, tag_end_position + tag_end_length, tag_definition['tag_end'])
								nested_tag_position = data.find("[" + tag_definition['tag'], nested_tag_position + 1 + tag_length)
							#
						#
					#
				#

				if (tag_end_position > -1):
				#
					if (self.log_handler != None): self.log_handler.debug("pas.tag_parser found '{0}' at {1:d}".format(tag_definition['tag'], data_position))
					data = self.parser_change(tag_definition, data, data_position, tag_start_end_position, tag_end_position)
				#
				else: data_position += tag_length
			#

			if (nested_check): data_position = -1
			else: data_position = data.find("[", data_position)
		#

		if (nested_check and tag_end_position < 0): data = None
		return data
	#

	def parser_change(self, tag_definition, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the matched tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:access: protected
:return: (str) Converted data
:since:  v0.1.00
		"""

		raise RuntimeError("Not implemented", 38)
	#

	def parser_check(self, data):
	#
		"""
Check if a possible tag match is a false positive.

:param data: Data starting with the possible tag

:access: protected
:return: (dict) Matched tag definition; None if false positive
:since:  v0.1.00
		"""

		return None
	#

	def parser_tag_end_find_position(self, data, data_position, tag_end):
	#
		"""
Find the starting position of the closing tag.

:param data: String that contains convertable data
:param data_position: Current parser position
:param tag_end: Tag end definition

:access: protected
:return: (int) Position; -1 if not found
:since:  v0.1.00
		"""

		var_return = None

		is_valid = True
		result = -1

		while ((var_return == None or var_return > -1) and is_valid):
		#
			result = data.find(tag_end, data_position)
			if (result > -1 and (var_return == None or result < var_return)): var_return = result

			if (var_return == None): var_return = -1
			elif (var_return > -1):
			#
				data_position = var_return
				if (data[var_return - 1:var_return] != "\\"): is_valid = False
			#
		#

		return var_return
	#

	def parser_tag_find_end_position(self, data, data_position):
	#
		"""
Find the starting position of the enclosing content.

:param data: String that contains convertable data
:param data_position: Current parser position

:access: protected
:return: (int) Position; -1 if not found
:since:  v0.1.00
		"""

		var_return = None

		is_valid = True

		while ((var_return == None or var_return > -1) and is_valid):
		#
			var_return = data.find("]", data_position)

			if (var_return > -1):
			#
				data_position = var_return
				if (data[var_return - 1:var_return] != "\\"): is_valid = False
			#
		#

		if (var_return > -1): var_return += 1
		return var_return
	#
#

##j## EOF