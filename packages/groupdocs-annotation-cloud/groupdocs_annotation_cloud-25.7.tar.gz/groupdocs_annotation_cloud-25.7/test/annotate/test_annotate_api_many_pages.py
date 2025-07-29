# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd">
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

from __future__ import absolute_import

import unittest
import os

from groupdocs_annotation_cloud import *
from test.test_context import TestContext
from test.test_file import TestFile

class TestAnnotateApiManyPages(TestContext):
    """AnnotateApi unit tests"""

    def test_add_annotate_many_pages(self):
        for test_file in TestFile.get_test_files_many_pages():
            file_info = FileInfo()
            file_info.file_path = test_file.folder + test_file.file_name
            file_info.password = test_file.password
            options = AnnotateOptions()
            options.file_info = file_info
            options.annotations = self.GetAnnotations()
            options.output_path = self.outputDir + "/" + test_file.file_name

            request = AnnotateRequest(options)
            result = self.annotate_api.annotate(request)            
            self.assertGreater(len(result['href']), 0)          
            
    @staticmethod
    def GetAnnotations():
        a1 = AnnotationInfo()
        a1.annotation_position = Point()
        a1.annotation_position.x = 852
        a1.annotation_position.y = 59.388262910798119
        a1.box = Rectangle()
        a1.box.x = 375.89276123046875
        a1.box.y = 59.388263702392578
        a1.box.width = 88.7330551147461
        a1.box.height = 37.7290153503418
        a1.page_number = 0
        a1.pen_color = 1201033
        a1.pen_style = "Solid"
        a1.pen_width = 1
        a1.type = "Distance"
        a1.creator_name = "Anonym A."

        a2 = AnnotationInfo()
        a2.annotation_position = Point()
        a2.annotation_position.x = 852
        a2.annotation_position.y = 59.388262910798119
        a2.box = Rectangle()
        a2.box.x = 375.89276123046875
        a2.box.y = 59.388263702392578
        a2.box.width = 88.7330551147461
        a2.box.height = 37.7290153503418
        a2.page_number = 2
        a2.pen_color = 1201033
        a2.pen_style = "Solid"
        a2.pen_width = 1
        a2.type = "Area"
        a2.creator_name = "Anonym A."

        a3 = AnnotationInfo()
        a3.annotation_position = Point()
        a3.annotation_position.x = 852
        a3.annotation_position.y = 59.388262910798119
        a3.box = Rectangle()
        a3.box.x = 375.89276123046875
        a3.box.y = 59.388263702392578
        a3.box.width = 88.7330551147461
        a3.box.height = 37.7290153503418
        a3.page_number = 3
        a3.type = "Point"
        a3.creator_name = "Anonym A."

        a4 = AnnotationInfo()
        a4.annotation_position = Point()
        a4.annotation_position.x = 852
        a4.annotation_position.y = 59.388262910798119
        a4.box = Rectangle()
        a4.box.x = 375.89276123046875
        a4.box.y = 59.388263702392578
        a4.box.width = 88.7330551147461
        a4.box.height = 37.7290153503418
        a4.page_number = 4
        a4.pen_color = 1201033
        a4.pen_style = "Solid"
        a4.pen_width = 1
        a4.type = "Arrow"
        a4.creator_name = "Anonym A."

        return [a1, a2, a3, a4]


if __name__ == '__main__':
    unittest.main()
