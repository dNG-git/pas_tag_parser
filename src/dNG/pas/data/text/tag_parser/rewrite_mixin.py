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

from dNG.pas.data.binary import Binary
from .source_value_mixin import SourceValueMixin

class RewriteMixin(SourceValueMixin):
#
	"""
This tag parser mixin provides support for rewrite statements.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: tag_parser
:since:      v0.1.01
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def render_rewrite(self, source, key):
	#
		"""
Renders the data identified by the given key.

:param source: Source for rewrite
:param key: Key in source for rewrite

:return: (str) Rendered content
:since:  v0.1.01
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_rewrite({1})- (#echo(__LINE__)#)", self, key, context = "pas_tag_parser")
		_return = self.get_source_value(source, key)

		_return = ("" if (_return is None) else Binary.str(_return))
		if (type(_return) is not str): _return = str(_return)

		return _return
	#
#

##j## EOF