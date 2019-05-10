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

# pylint: disable=import-error, no-name-in-module

import re

from dpt_runtime.not_implemented_exception import NotImplementedException

class Abstract(object):
    """
The abstract parser implements methods to find and process "[tags]".

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: tag_parser
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=unused-argument

    RE_ESCAPED = re.compile("(\\\\+)$")
    """
RegExp to identify escaped values
    """

    def __init__(self):
        """
Constructor __init__(Abstract)

:since: v1.0.0
        """

        self._log_handler = None
        """
The LogHandler is called whenever debug messages should be logged or errors
happened.
        """
    #

    def _find_newlines_block_position(self, data, data_position, newlines_max):
        """
Moves the given position to include the additional number of newline
characters given.

:param data: String that contains data
:param data_position: Current parser position
:param newlines_max: Newline characters before (<0) or after the given position

:return: (int) Calculated position
:since:  v1.0.0
        """

        _return = data_position

        data_length = len(data)
        direction = 1

        if (newlines_max < 0):
            direction = -1
            newlines_max *= -1
        #

        for character_position in range(0, newlines_max):
            if (direction > 0):
                position_start = _return
                position_end = _return + direction
            else:
                position_start = _return + direction
                position_end = _return
            #

            if (_return < 1 or _return >= data_length or data[position_start:position_end] != "\n"): break
            else: _return += direction
        #

        return _return
    #

    def _find_end_tag_position(self, data, data_position, tag_end):
        """
Find the starting position of the closing tag.

:param data: String that contains convertable data
:param data_position: Current parser position
:param tag_end: Tag end definition

:return: (int) Position; -1 if not found
:since:  v1.0.0
        """

        _return = None

        result = -1

        while (_return is None or _return > -1):
            result = data.find(tag_end, data_position)
            if (result > -1 and (_return is None or result < _return)): _return = result

            if (_return is None): _return = -1
            elif (_return > -1):
                data_position = _return
                if (data[_return - 1:_return] != "\\"): break
            #
        #

        return _return
    #

    def _find_tag_end_position(self, data, data_position):
        """
Find the starting position of the enclosing content.

:param data: String that contains convertable data
:param data_position: Current parser position

:return: (int) Position; -1 if not found
:since:  v1.0.0
        """

        _return = None

        while (_return is None or _return > -1):
            _return = data.find("]", data_position)

            if (_return > -1):
                data_position = _return
                if (data[_return - 1:_return] != "\\"): break
            #
        #

        if (_return > -1): _return += 1
        return _return
    #

    def _change_match(self, tag_definition, data, tag_position, data_position, tag_end_position):
        """
Change data according to the matched tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v1.0.0
        """

        position = tag_position

        if (tag_definition.get("newlines_before_block", 0) > 0):
            position = self._find_newlines_block_position(data, position, -1 * tag_definition['newlines_before_block'])
        #

        _return = data[:position]

        method = getattr(self, "_change_match_{0}".format(tag_definition['tag']), None)

        if (method is not None): _return += method(data, tag_position, data_position, tag_end_position)

        if (tag_definition.get("type") != "simple"):
            position = self._find_tag_end_position(data, tag_end_position)

            if (tag_definition.get("newlines_after_block", 0) > 0):
                position = self._find_newlines_block_position(data, position, tag_definition['newlines_after_block'])
            #

            _return += data[position:]
        #

        return _return
    #

    def _check_match(self, data):
        """
Check if a possible tag match is a false positive.

:param data: Data starting with the possible tag

:return: (dict) Matched tag definition; None if false positive
:since:  v1.0.0
        """

        return None
    #

    def _parse(self, data, data_position = 0, nested_tag_end_position = None):
        """
Parse for "[tags]" and calls "_check_match()" for possible hits.

:param data: Data to be parsed
:param data_position: Current parser position
:param nested_tag_end_position: End position for nested tags

:return: (bool) True if replacements happened
:since:  v1.0.0
        """

        if (nested_tag_end_position is None):
            data_position = data.find("[", data_position)
            nested_check = False
        else:
            data_position = data.find("[", data_position)
            if (data_position >= nested_tag_end_position): data_position = -1

            nested_check = True
            tag_end_position = -1
        #

        while (data_position > -1):
            tag_definition = self._check_match(data[data_position:])

            if (tag_definition is None): data_position += 1
            else:
                is_simple_tag = (tag_definition.get("type") == "simple")
                is_valid = False
                tag_length = len(tag_definition['tag'])

                tag_element_end_position = self._find_tag_end_position(data, data_position + 1 + tag_length)
                tag_end_position = -1

                if (is_simple_tag): is_valid = (tag_element_end_position > -1)
                elif (tag_element_end_position > -1):
                    tag_end_position = self._find_end_tag_position(data, tag_element_end_position, tag_definition['tag_end'])

                    if (tag_end_position >= 0):
                        method = (self._parse_nested_walker
                                  if ("type" not in tag_definition or tag_definition['type'] != "top_down") else
                                  self._parse_top_down_walker
                                 )

                        ( data,
                          tag_element_end_position,
                          tag_end_position
                        ) = method(data, data_position, tag_definition, tag_element_end_position, tag_end_position)

                        is_valid = (tag_element_end_position > -1 and tag_end_position > -1)
                    #
                #

                if (is_valid):
                    if (self._log_handler is not None): self._log_handler.debug("{0!r} found '{1}' at {2:d}", self, tag_definition['tag'], data_position, context = "pas_tag_parser")
                    data = self._change_match(tag_definition, data, data_position, tag_element_end_position, tag_end_position)
                else: data_position += tag_length
            #

            if (tag_definition is not None and nested_check): data_position = -1
            else: data_position = data.find("[", data_position)
        #

        if (nested_check and tag_end_position < 0): data = None
        return data
    #

    def _parse_nested_walker(self, data, data_position, tag_definition, tag_element_end_position, tag_end_position):
        """
Parse nested tags recursively.

:param data: Data to be parsed
:param data_position: Current parser position
:param tag_definition: Matched tag definition
:param tag_element_end_position: Starting position of the enclosing content
:param tag_end_position: Starting position of the closing tag

:return: (tuple) New data and positions values
:since:  v1.0.0
        """

        nested_data = self._parse(data, data_position + 1, tag_end_position)

        while (nested_data is not None):
            data = nested_data
            tag_element_end_position_new = self._find_tag_end_position(data, data_position + 1)

            if (tag_element_end_position_new > -1):
                tag_end_position = self._find_end_tag_position(data, tag_element_end_position_new, tag_definition['tag_end'])
                tag_element_end_position = tag_element_end_position_new
            #

            nested_data = self._parse(data, data_position + 1, tag_end_position)
        #

        return ( data, tag_element_end_position, tag_end_position )
    #

    def _parse_top_down_walker(self, data, data_position, tag_definition, tag_element_end_position, tag_end_position):
        """
Parse nested tags of the same type to find the correct end position.

:param data: Data to be parsed
:param data_position: Current parser position
:param tag_definition: Matched tag definition
:param tag_element_end_position: Starting position of the enclosing content
:param tag_end_position: Starting position of the closing tag

:return: (tuple) New data and positions values
:since:  v1.0.0
        """

        tag_length = len(tag_definition['tag'])

        is_nested = False
        nested_tag_position = data.find("[" + tag_definition['tag'], data_position + 1 + tag_length)
        tag_end_length = len(tag_definition['tag_end'])

        while (nested_tag_position >= 0 and nested_tag_position < tag_end_position):
            is_nested = True

            if (self._check_match(data[nested_tag_position:]) is not None):
                tag_end_position = self._find_end_tag_position(data, tag_end_position + tag_end_length, tag_definition['tag_end'])
            #

            nested_tag_position = data.find("[" + tag_definition['tag'], nested_tag_position + 1 + tag_length)
        #

        if (is_nested): tag_element_end_position = self._find_tag_end_position(data, data_position + 1)

        return ( data, tag_element_end_position, tag_end_position )
    #

    @staticmethod
    def parse_tag_parameters(tag_key, data, tag_position, data_position):
        """
Check if a possible tag matches the given expected, simple tag.

:param tag_key: Tag key
:param data: Data starting with the possible tag
:param tag_position: Tag starting position
:param data_position: Data starting position

:return: (bool) True if valid
:since:  v1.0.0
        """

        _return = { }

        data_splitted = data[1 + len(tag_key) + tag_position:data_position - 1].split(":", 1)

        data = (data_splitted[0] if (len(data_splitted[0]) > 0 or len(data_splitted) > 1) else None)
        value = ""

        while (data is not None):
            if (len(data) > 0):
                re_result = Abstract.RE_ESCAPED.search(data)
                value += data

                if (re_result is None or (len(re_result.group(1)) % 2) != 1):
                    value_splitted = value.split("=", 1)

                    if (len(value_splitted) > 1):
                        key = (tag_key if (value_splitted[0] == "") else value_splitted[0])
                        value = value_splitted[1]
                    else: key = tag_key

                    if (key not in _return): _return[key] = value
                    value = ""
                #
            #

            if (len(data_splitted) > 1):
                data_splitted = data_splitted[1].split(":", 1)
                data = data_splitted[0]
            else: break
        #

        return _return
    #
#
