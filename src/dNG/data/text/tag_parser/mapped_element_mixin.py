# -*- coding: utf-8 -*-

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

class MappedElementMixin(object):
    """
This tag parser mixin provides support for mapping elements for loops.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: tag_parser
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self):
        """
Constructor __init__(MappedElementMixin)

:since: v1.0.0
        """

        self.mapped_data = { }
        """
Dict with mapped data
        """
    #

    def _remove_mapped_element(self, key, source = None):
        """
Removed the mapped element from the source.

:param key: Multi-dimensional key in source separated by "."
:param source: Source where value will be removed

:since: v1.0.0
        """

        if (source is None): source = self.mapped_data

        if (isinstance(source, dict)):
            key_list = key.split(".", 1)

            if (key_list[0] in source):
                if (len(key_list) > 1):
                    self._remove_mapped_element(key_list[1], source[key_list[0]])
                    if (len(source[key_list[0]]) < 1): del(source[key_list[0]])
                else: del(source[key])
            #
        #
    #

    def _set_mapped_element(self, key, value, source = None):
        """
Sets the mapped element key to the given value.

:param key: Multi-dimensional key in source separated by "."
:param source: Source where value will be set as key

:since: v1.0.0
        """

        if (source is None): source = self.mapped_data

        if (isinstance(source, dict)):
            key_list = key.split(".", 1)

            if (len(key_list) > 1):
                if (key_list[0] not in source): source[key_list[0]] = { }
                self._set_mapped_element(key_list[1], value, source[key_list[0]])
            else: source[key] = value
        #
    #

    def _update_mapped_element(self, key, source):
        """
Updates the source with the mapped element identified by the given key.

:param key: Key of the mapped element
:param source: Source where the mapped element will be included

:return: Source including the mapped element
:since:  v1.0.0
        """

        if (key in self.mapped_data): return self._update_mapped_element_walker(self.mapped_data[key], source.copy())
        else: return source
    #

    def _update_mapped_element_walker(self, source, target):
        """
Updates the source recursively with the mapped element identified by the
given key.

:param source: Source that should be mapped to target
:param target: Mapped dict

:return: Target with the source applied
:since:  v1.0.0
        """

        for key in source:
            if (isinstance(source[key], dict)):
                if (key in target): target[key] = self._update_mapped_element_walker(source[key], (target[key] if (isinstance(target[key], dict)) else { }))
                else: target[key] = self._update_mapped_element_walker(source[key], { })
            else: target[key] = source[key]
        #

        return target
    #
#
