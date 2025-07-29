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

from groupdocs_annotation_cloud import *
from test.test_context import TestContext
from test.test_file import TestFile

class TestInfoApi(TestContext):
    """InfoApi unit tests"""

    def test_get_supported_file_formats(self):
        data = self.info_api.get_supported_file_formats()

        for format in data.formats:
            self.assertFalse(format.file_format == "")
            self.assertFalse(format.extension == "")
    
    def test_get_info(self):
        for test_file in TestFile.get_test_files_annotation():
            file_info = FileInfo()
            file_info.file_path = test_file.folder + test_file.file_name
            file_info.password = test_file.password

            request = GetInfoRequest(file_info)
            response = self.info_api.get_info(request)
            self.assertEqual(file_info.file_path, response.path)
            self.assertGreater(len(response.pages), 0)

    def test_get_info_returns_file_not_found(self):
        file_info = FileInfo()
        file_info.file_path = "somefolder\\not-exist.docx"

        request = GetInfoRequest(file_info)
        with self.assertRaises(ApiException) as context:
            self.info_api.get_info(request)
        self.assertEqual("Specified file not found", context.exception.message)

if __name__ == '__main__':
    unittest.main()
