# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.tag_parser.SourceValueMixin
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

class SourceValueMixin(object):
#
	"""
This tag parser mixin provides support to find a key in a given source dict.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: tag_parser
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def source_get_value(self, source, key):
	#
		"""
Checks and renders the rewrite statement.

:param source: Source for rewrite
:param key: Key in source for rewrite

:return: (str) Rewritten statement if successful
:since:  v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.source_get_value(source, {1})- (#echo(__LINE__)#)".format(self, key))
		_return = None

		if (isinstance(source, dict)):
		#
			key_list = key.split(".", 1)

			if (key_list[0] in source):
			#
				if (len(key_list) > 1): _return = self.source_get_value(source[key_list[0]], key_list[1])
				else: _return = source[key]
			#
		#

		return _return
	#
#

##j## EOF