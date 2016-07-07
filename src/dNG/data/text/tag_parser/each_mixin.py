# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;tag_parser

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasTagParserVersion)#
#echo(__FILEPATH__)#
"""

from .mapped_element_mixin import MappedElementMixin
from .source_value_mixin import SourceValueMixin

class EachMixin(MappedElementMixin, SourceValueMixin):
#
	"""
This tag parser mixin provides support for each loop statements.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: tag_parser
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def render_each(self, data, source_key, source, key, mapping_key):
	#
		"""
Checks and renders the each statement.

:param data: Element template data
:param source_key: Originating source key
:param source: Source for comparison
:param key: Key in source for comparison
:param mapping_key: Element mapping key

:return: (str) Rewritten statement if successful
:since:  v0.2.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_each({1}, {2}, {3})- (#echo(__LINE__)#)", self, source_key, key, mapping_key, context = "pas_tag_parser")
		_return = ""

		elements = self.get_source_value(source, key)

		if (isinstance(elements, list)):
		#
			for element in elements:
			#
				element_mapped_key = "{0}.{1}.{2}".format(source_key, key, mapping_key)
				self._set_mapped_element(element_mapped_key, element)

				try: _return += self._parse(data)
				finally: self._remove_mapped_element(element_mapped_key)
			#
		#

		return _return
	#
#

##j## EOF