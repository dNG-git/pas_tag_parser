# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.tag_parser.IfConditionMixin
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

from dNG.pas.data.binary import Binary
from .source_value_mixin import SourceValueMixin

class IfConditionMixin(SourceValueMixin):
#
	"""
This tag parser mixin provides support for if conditions.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: tag_parser
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def render_if_condition(self, source, key, operator, value, data):
	#
		"""
Checks and renders the content of the "if" condition.

:param data: Conditional data
:param source: Source for comparison
:param key: Key in source for comparison
:param operator: Comparison operator
:param value: Comparison value

:return: (str) Conditional data if successful
:since:  v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_if_condition(source, {1}, {2}, {3}, data)- (#echo(__LINE__)#)".format(self, key, operator, value))
		_return = ""

		is_valid = False
		source_value = self.source_get_value(source, key)

		source_value = ("" if (source_value == None) else Binary.str(source_value))
		if (type(source_value) != str): source_value = str(source_value)

		if (operator == "==" and source_value == value): is_valid = True
		if (operator == "!=" and source_value != value): is_valid = True

		if (is_valid): _return = data
		return _return
	#
#

##j## EOF