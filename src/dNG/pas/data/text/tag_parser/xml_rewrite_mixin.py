# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.tag_parser.XmlRewriteMixin
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

class XmlRewriteMixin(object):
#
	"""
This tag parser mixin provides support for XML based rewrite statements.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: tag_parser
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def render_xml_rewrite(self, xml_parser, xml_base_path, xml_value_path):
	#
		"""
Checks and renders the rewrite statement.

:param source: Source for rewrite
:param key: Key in source for rewrite

:return: (str) Rewritten statement if successful
:since:  v0.1.01
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_xml_rewrite(xml_parser, {1}, {2})- (#echo(__LINE__)#)".format(self, xml_base_path, xml_value_path))
		_return = xml_parser.get_node_value("{0} {1}".format(xml_base_path, xml_value_path))

		_return = (" {0} ".format(xml_value_path) if (_return == None) else Binary.str(_return))
		if (type(_return) != str): _return = str(_return)

		return _return
	#
#

##j## EOF