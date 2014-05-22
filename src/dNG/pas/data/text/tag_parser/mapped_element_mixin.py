# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.tag_parser.MappedElementMixin
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

class MappedElementMixin(object):
#
	"""
This tag parser mixin provides support for mapping elements for loops.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: tag_parser
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(MappedElementMixin)

:since: v0.1.01
		"""

		self.mapped_data = { }
		"""
Dict with mapped data
		"""
	#

	def _remove_mapped_element(self, key, source = None):
	#
		"""
Checks and renders the rewrite statement.

:param source: Source for rewrite
:param key: Key in source for rewrite

:since: v0.1.01
		"""

		if (source == None): source = self.mapped_data

		if (isinstance(source, dict)):
		#
			key_list = key.split(".", 1)

			if (key_list[0] in source):
			#
				if (len(key_list) > 1):
				#
					self._remove_mapped_element(key_list[1], source[key_list[0]])
					if (len(source[key_list[0]]) < 1): del(source[key_list[0]])
				#
				else: del(source[key])
			#
		#
	#

	def _set_mapped_element(self, key, value, source = None):
	#
		"""
Checks and renders the rewrite statement.

:param source: Source for rewrite
:param key: Key in source for rewrite

:since: v0.1.01
		"""

		if (source == None): source = self.mapped_data

		if (isinstance(source, dict)):
		#
			key_list = key.split(".", 1)

			if (len(key_list) > 1):
			#
				if (key_list[0] not in source): source[key_list[0]] = { }
				self._set_mapped_element(key_list[1], value, source[key_list[0]])
			#
			else: source[key] = value
		#
	#

	def _update_mapped_element(self, key, source):
	#
		"""
Checks and renders the rewrite statement.

:param source: Source for rewrite
:param key: Key in source for rewrite

:since: v0.1.01
		"""

		if (key in self.mapped_data): return self._update_mapped_element_walker(self.mapped_data[key], source.copy())
		else: return source
	#

	def _update_mapped_element_walker(self, source, target):
	#
		"""
Checks and renders the rewrite statement.

:param source: Source for rewrite
:param key: Key in source for rewrite

:since: v0.1.01
		"""

		for key in source:
		#
			if (isinstance(source[key], dict)):
			#
				if (key in target): target[key] = self._update_mapped_element_walker(source[key], (target[key] if (isinstance(target[key], dict)) else { }))
				else: target[key] = self._update_mapped_element_walker(source[key], { })
			#
			else: target[key] = source[key]
		#

		return target
	#
#

##j## EOF