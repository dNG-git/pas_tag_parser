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

from dNG.data.binary import Binary

class XmlRewriteMixin(object):
#
	"""
This tag parser mixin provides support for XML based rewrite statements.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: tag_parser
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def render_xml_rewrite(self, xml_resource, xml_base_path, xml_value_path):
	#
		"""
Renders the data identified by the given node value path in the XML
resource.

:param xml_resource: XML resource instance
:param xml_base_path: XML base node path
:param xml_value_path: XML value node path

:return: (str) Rendered content
:since:  v0.2.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_xml_rewrite({1}, {2})- (#echo(__LINE__)#)", self, xml_base_path, xml_value_path, context = "pas_tag_parser")
		_return = xml_resource.get_node_value("{0} {1}".format(xml_base_path, xml_value_path))

		_return = ("" if (_return is None) else Binary.str(_return))
		if (type(_return) is not str): _return = str(_return)

		return _return
	#
#

##j## EOF