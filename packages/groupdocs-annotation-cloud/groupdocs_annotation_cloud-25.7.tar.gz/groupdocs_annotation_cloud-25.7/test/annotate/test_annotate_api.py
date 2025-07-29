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

class TestAnnotateApi(TestContext):
    """AnnotateApi unit tests"""

    def test_add_annotate(self):
        for test_file in TestFile.get_test_files_annotation():
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

    def test_add_annotate_direct(self):
        for test_file in TestFile.get_test_files_annotation():
            file_info = FileInfo()
            file_info.file_path = test_file.folder + test_file.file_name
            file_info.password = test_file.password
            options = AnnotateOptions()
            options.file_info = file_info
            options.annotations = self.GetAnnotations()
            options.output_path = self.outputDir + "/" + test_file.file_name

            request = AnnotateDirectRequest(options)
            result = self.annotate_api.annotate_direct(request)            
            self.assertGreater(len(result), 0)

    def test_extract(self):
        for test_file in TestFile.get_test_files_with_annotations():
            file_info = FileInfo()
            file_info.file_path = test_file.folder + test_file.file_name
            file_info.password = test_file.password

            request = ExtractRequest(file_info)
            result = self.annotate_api.extract(request)            
            self.assertGreater(len(result), 0)

    def test_remove_annotations(self):
        for test_file in TestFile.get_test_files_with_annotations():
            file_info = FileInfo()
            file_info.file_path = test_file.folder + test_file.file_name
            file_info.password = test_file.password
            options = RemoveOptions()
            options.file_info = file_info
            options.annotation_ids = [1, 2, 3]
            options.output_path = self.outputDir + "/" + test_file.file_name

            request = RemoveAnnotationsRequest(options)
            result = self.annotate_api.remove_annotations(request)            
            self.assertGreater(len(result['href']), 0)
            
    @staticmethod
    def GetAnnotations():
        a = AnnotationInfo()
        a.annotation_position = Point()
        a.annotation_position.x = 852
        a.annotation_position.y = 59.388262910798119
        a.box = Rectangle()
        a.box.x = 375.89276123046875
        a.box.y = 59.388263702392578
        a.box.width = 88.7330551147461
        a.box.height = 37.7290153503418
        a.page_number = 0
        a.pen_color = 1201033
        a.pen_style = "Solid"
        a.pen_width = 1
        a.type = "Area"
        a.creator_name = "Anonym A."
        return [a]


if __name__ == '__main__':
    unittest.main()
