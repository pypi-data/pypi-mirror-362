# GroupDocs.Annotation Cloud Python SDK

Python package for communicating with the GroupDocs.Annotation Cloud API

## Requirements

Python 2.7 or 3.4+

## Installation

Install `groupdocs-annotation-cloud` with [PIP](https://pypi.org/project/pip/) from [PyPI](https://pypi.org/) by:

```sh
pip install groupdocs-annotation-cloud
```

Or clone repository and install it via [Setuptools](http://pypi.python.org/pypi/setuptools):

```sh
python setup.py install
```

## Getting Started

Please follow the [installation procedure](#installation) and then run following:

```python
# Import module
import groupdocs_annotation_cloud

# Get your app_sid and app_key at https://dashboard.groupdocs.cloud (free registration is required).
app_sid = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
app_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Create instance of the API
api = groupdocs_annotation_cloud.InfoApi.from_keys(app_sid, app_key)

try:
    # Retrieve supported file-formats
    response = api.get_supported_file_formats()

    # Print out supported file-formats
    print("Supported file-formats:")
    for format in response.formats:
        print('{0} ({1})'.format(format.file_format, format.extension))
except groupdocs_annotation_cloud.ApiException as e:
    print("Exception when calling get_supported_file_formats: {0}".format(e.message))
```

## Licensing

GroupDocs.Annotation Cloud Python SDK licensed under [MIT License](http://github.com/groupdocs-annotation-cloud/groupdocs-annotation-cloud-python/LICENSE).

## Resources

+[**Website**](https://www.groupdocs.cloud)
+[**Product Home**](https://products.groupdocs.cloud/annotation)
+[**Documentation**](https://docs.groupdocs.cloud/annotation/)
+[**Free Support Forum**](https://forum.groupdocs.cloud/c/annotation)
+[**Blog**](https://blog.groupdocs.cloud/category/annotation)

## Contact Us

Your feedback is very important to us. Please feel free to contact us using our [Support Forums](https://forum.groupdocs.cloud/c/annotation).
