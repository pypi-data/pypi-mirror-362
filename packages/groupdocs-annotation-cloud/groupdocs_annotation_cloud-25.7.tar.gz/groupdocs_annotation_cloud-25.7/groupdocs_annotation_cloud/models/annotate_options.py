# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="AnnotateOptions.py">
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

class AnnotateOptions(object):
    """
    Defines options for annotating documents
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
        'annotations': 'list[AnnotationInfo]',
        'first_page': 'int',
        'last_page': 'int',
        'only_annotated_pages': 'bool',
        'output_path': 'str',
        'fonts_path': 'str'
    }

    attribute_map = {
        'file_info': 'FileInfo',
        'annotations': 'Annotations',
        'first_page': 'FirstPage',
        'last_page': 'LastPage',
        'only_annotated_pages': 'OnlyAnnotatedPages',
        'output_path': 'OutputPath',
        'fonts_path': 'FontsPath'
    }

    def __init__(self, file_info=None, annotations=None, first_page=None, last_page=None, only_annotated_pages=None, output_path=None, fonts_path=None, **kwargs):  # noqa: E501
        """Initializes new instance of AnnotateOptions"""  # noqa: E501

        self._file_info = None
        self._annotations = None
        self._first_page = None
        self._last_page = None
        self._only_annotated_pages = None
        self._output_path = None
        self._fonts_path = None

        if file_info is not None:
            self.file_info = file_info
        if annotations is not None:
            self.annotations = annotations
        if first_page is not None:
            self.first_page = first_page
        if last_page is not None:
            self.last_page = last_page
        if only_annotated_pages is not None:
            self.only_annotated_pages = only_annotated_pages
        if output_path is not None:
            self.output_path = output_path
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
    def annotations(self):
        """
        Gets the annotations.  # noqa: E501

        List of annotations to add to the document  # noqa: E501

        :return: The annotations.  # noqa: E501
        :rtype: list[AnnotationInfo]
        """
        return self._annotations

    @annotations.setter
    def annotations(self, annotations):
        """
        Sets the annotations.

        List of annotations to add to the document  # noqa: E501

        :param annotations: The annotations.  # noqa: E501
        :type: list[AnnotationInfo]
        """
        self._annotations = annotations
    
    @property
    def first_page(self):
        """
        Gets the first_page.  # noqa: E501

        First page number when saving page range  # noqa: E501

        :return: The first_page.  # noqa: E501
        :rtype: int
        """
        return self._first_page

    @first_page.setter
    def first_page(self, first_page):
        """
        Sets the first_page.

        First page number when saving page range  # noqa: E501

        :param first_page: The first_page.  # noqa: E501
        :type: int
        """
        if first_page is None:
            raise ValueError("Invalid value for `first_page`, must not be `None`")  # noqa: E501
        self._first_page = first_page
    
    @property
    def last_page(self):
        """
        Gets the last_page.  # noqa: E501

        Last page number when saving page range  # noqa: E501

        :return: The last_page.  # noqa: E501
        :rtype: int
        """
        return self._last_page

    @last_page.setter
    def last_page(self, last_page):
        """
        Sets the last_page.

        Last page number when saving page range  # noqa: E501

        :param last_page: The last_page.  # noqa: E501
        :type: int
        """
        if last_page is None:
            raise ValueError("Invalid value for `last_page`, must not be `None`")  # noqa: E501
        self._last_page = last_page
    
    @property
    def only_annotated_pages(self):
        """
        Gets the only_annotated_pages.  # noqa: E501

        Indicates whether to save only annotated pages  # noqa: E501

        :return: The only_annotated_pages.  # noqa: E501
        :rtype: bool
        """
        return self._only_annotated_pages

    @only_annotated_pages.setter
    def only_annotated_pages(self, only_annotated_pages):
        """
        Sets the only_annotated_pages.

        Indicates whether to save only annotated pages  # noqa: E501

        :param only_annotated_pages: The only_annotated_pages.  # noqa: E501
        :type: bool
        """
        if only_annotated_pages is None:
            raise ValueError("Invalid value for `only_annotated_pages`, must not be `None`")  # noqa: E501
        self._only_annotated_pages = only_annotated_pages
    
    @property
    def output_path(self):
        """
        Gets the output_path.  # noqa: E501

        Path to output document in the cloud storage. Required for Add method. Not required if Annotate (with file result) method used.  # noqa: E501

        :return: The output_path.  # noqa: E501
        :rtype: str
        """
        return self._output_path

    @output_path.setter
    def output_path(self, output_path):
        """
        Sets the output_path.

        Path to output document in the cloud storage. Required for Add method. Not required if Annotate (with file result) method used.  # noqa: E501

        :param output_path: The output_path.  # noqa: E501
        :type: str
        """
        self._output_path = output_path
    
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
        if not isinstance(other, AnnotateOptions):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
