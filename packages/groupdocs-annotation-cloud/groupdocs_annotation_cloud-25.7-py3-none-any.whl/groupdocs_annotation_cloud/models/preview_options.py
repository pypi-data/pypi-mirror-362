# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="PreviewOptions.py">
#   Copyright (c) Aspose Pty Ltd
# </copyright>
# <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# -----------------------------------------------------------------------------------

import pprint
import re  # noqa: F401

import six

class PreviewOptions(object):
    """
    Represents options for GetPages API method
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'file_info': 'FileInfo',
        'format': 'str',
        'page_numbers': 'list[int]',
        'width': 'int',
        'height': 'int',
        'resolution': 'int',
        'render_comments': 'bool',
        'render_annotations': 'bool',
        'fonts_path': 'str'
    }

    attribute_map = {
        'file_info': 'FileInfo',
        'format': 'Format',
        'page_numbers': 'PageNumbers',
        'width': 'Width',
        'height': 'Height',
        'resolution': 'Resolution',
        'render_comments': 'RenderComments',
        'render_annotations': 'RenderAnnotations',
        'fonts_path': 'FontsPath'
    }

    def __init__(self, file_info=None, format=None, page_numbers=None, width=None, height=None, resolution=None, render_comments=None, render_annotations=None, fonts_path=None, **kwargs):  # noqa: E501
        """Initializes new instance of PreviewOptions"""  # noqa: E501

        self._file_info = None
        self._format = None
        self._page_numbers = None
        self._width = None
        self._height = None
        self._resolution = None
        self._render_comments = None
        self._render_annotations = None
        self._fonts_path = None

        if file_info is not None:
            self.file_info = file_info
        if format is not None:
            self.format = format
        if page_numbers is not None:
            self.page_numbers = page_numbers
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if resolution is not None:
            self.resolution = resolution
        if render_comments is not None:
            self.render_comments = render_comments
        if render_annotations is not None:
            self.render_annotations = render_annotations
        if fonts_path is not None:
            self.fonts_path = fonts_path
    
    @property
    def file_info(self):
        """
        Gets the file_info.  # noqa: E501

        Input document description  # noqa: E501

        :return: The file_info.  # noqa: E501
        :rtype: FileInfo
        """
        return self._file_info

    @file_info.setter
    def file_info(self, file_info):
        """
        Sets the file_info.

        Input document description  # noqa: E501

        :param file_info: The file_info.  # noqa: E501
        :type: FileInfo
        """
        self._file_info = file_info
    
    @property
    def format(self):
        """
        Gets the format.  # noqa: E501

        Preview format. Supported values are: PNG, JPEG or BMP. Default value is PNG.  # noqa: E501

        :return: The format.  # noqa: E501
        :rtype: str
        """
        return self._format

    @format.setter
    def format(self, format):
        """
        Sets the format.

        Preview format. Supported values are: PNG, JPEG or BMP. Default value is PNG.  # noqa: E501

        :param format: The format.  # noqa: E501
        :type: str
        """
        if format is None:
            raise ValueError("Invalid value for `format`, must not be `None`")  # noqa: E501
        allowed_values = ["PNG", "JPEG", "BMP"]  # noqa: E501
        if not format.isdigit():	
            if format not in allowed_values:
                raise ValueError(
                    "Invalid value for `format` ({0}), must be one of {1}"  # noqa: E501
                    .format(format, allowed_values))
            self._format = format
        else:
            self._format = allowed_values[int(format) if six.PY3 else long(format)]
    
    @property
    def page_numbers(self):
        """
        Gets the page_numbers.  # noqa: E501

        Page numbers to preview. All pages proceeded if not specified.  # noqa: E501

        :return: The page_numbers.  # noqa: E501
        :rtype: list[int]
        """
        return self._page_numbers

    @page_numbers.setter
    def page_numbers(self, page_numbers):
        """
        Sets the page_numbers.

        Page numbers to preview. All pages proceeded if not specified.  # noqa: E501

        :param page_numbers: The page_numbers.  # noqa: E501
        :type: list[int]
        """
        self._page_numbers = page_numbers
    
    @property
    def width(self):
        """
        Gets the width.  # noqa: E501

        Preview image width. Not required. Default width used if not specified or 0.  # noqa: E501

        :return: The width.  # noqa: E501
        :rtype: int
        """
        return self._width

    @width.setter
    def width(self, width):
        """
        Sets the width.

        Preview image width. Not required. Default width used if not specified or 0.  # noqa: E501

        :param width: The width.  # noqa: E501
        :type: int
        """
        if width is None:
            raise ValueError("Invalid value for `width`, must not be `None`")  # noqa: E501
        self._width = width
    
    @property
    def height(self):
        """
        Gets the height.  # noqa: E501

        Preview image height. Not required. Default width used if not specified or 0.  # noqa: E501

        :return: The height.  # noqa: E501
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """
        Sets the height.

        Preview image height. Not required. Default width used if not specified or 0.  # noqa: E501

        :param height: The height.  # noqa: E501
        :type: int
        """
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")  # noqa: E501
        self._height = height
    
    @property
    def resolution(self):
        """
        Gets the resolution.  # noqa: E501

        Gets or sets the resolution for generated images, in dots per inch. The default value is 96.  # noqa: E501

        :return: The resolution.  # noqa: E501
        :rtype: int
        """
        return self._resolution

    @resolution.setter
    def resolution(self, resolution):
        """
        Sets the resolution.

        Gets or sets the resolution for generated images, in dots per inch. The default value is 96.  # noqa: E501

        :param resolution: The resolution.  # noqa: E501
        :type: int
        """
        if resolution is None:
            raise ValueError("Invalid value for `resolution`, must not be `None`")  # noqa: E501
        self._resolution = resolution
    
    @property
    def render_comments(self):
        """
        Gets the render_comments.  # noqa: E501

        Render document comments. Default value is 'false'.  # noqa: E501

        :return: The render_comments.  # noqa: E501
        :rtype: bool
        """
        return self._render_comments

    @render_comments.setter
    def render_comments(self, render_comments):
        """
        Sets the render_comments.

        Render document comments. Default value is 'false'.  # noqa: E501

        :param render_comments: The render_comments.  # noqa: E501
        :type: bool
        """
        if render_comments is None:
            raise ValueError("Invalid value for `render_comments`, must not be `None`")  # noqa: E501
        self._render_comments = render_comments
    
    @property
    def render_annotations(self):
        """
        Gets the render_annotations.  # noqa: E501

        The property that controls whether annotations will be generated on the preview. Default State - true.  # noqa: E501

        :return: The render_annotations.  # noqa: E501
        :rtype: bool
        """
        return self._render_annotations

    @render_annotations.setter
    def render_annotations(self, render_annotations):
        """
        Sets the render_annotations.

        The property that controls whether annotations will be generated on the preview. Default State - true.  # noqa: E501

        :param render_annotations: The render_annotations.  # noqa: E501
        :type: bool
        """
        if render_annotations is None:
            raise ValueError("Invalid value for `render_annotations`, must not be `None`")  # noqa: E501
        self._render_annotations = render_annotations
    
    @property
    def fonts_path(self):
        """
        Gets the fonts_path.  # noqa: E501

        The path to directory containing custom fonts in storage  # noqa: E501

        :return: The fonts_path.  # noqa: E501
        :rtype: str
        """
        return self._fonts_path

    @fonts_path.setter
    def fonts_path(self, fonts_path):
        """
        Sets the fonts_path.

        The path to directory containing custom fonts in storage  # noqa: E501

        :param fonts_path: The fonts_path.  # noqa: E501
        :type: str
        """
        self._fonts_path = fonts_path

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PreviewOptions):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
