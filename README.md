# DocumentationSync

A Python library that builds DocC Documentation archive files for Swift Packages, Xcode projects, or XCFrameworks, and uploads internal library documentation to Confluence.

## Tech Lead/Owner
Coleton Gorecke, cgorecke@firstorion.com

## Purpose
This library helps sync the README.md, Changelog.md, and .doccarchive files for internal libraries with their respective page in Confluence.

## Requirements
Python 3.5 or greater

If building documentation for a Swift Package or Framework, you must make sure [Apple's DocC library](https://github.com/apple/swift-docc-plugin) is added as a dependency.

## Dependencies
- pathlib: introduced in Python 3.4
- typing: introduced in Python 3.5
- requests: version 2.0.0+
- markdown: version 3.0.0+

## Installation
1. Create an API Key
[Manage Confluence API Keys](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)
2. Determine SpaceID for the space to update via Space Admin.
3. Install any dependencies using:
```pip install <dependency>```
4. CD to the directory where the script is located and use:
```python3 <repo_file_path> <repo_name>```

This library requires some setup from Confluence and should be configured in the ConfluenceUploader/config.py.

```
Example: 'https://yoursite.net/wiki/api/v2'
CONFLUENCE_BASE_URL = 'your-base-url'
```

```
Example: 'cgorecke@firstorion.com'
CONFLUENCE_EMAIL = 'your-email'
```

```
Example: 'ATATT....'
CONFLUENCE_API_KEY = 'your-api-key'
```

```
Example: This is the mobile eng space id: '800260186'.
CONFLUENCE_SPACE_KEY = 'confluence-space-key'
```

## Supported Documentation Types
To build and sync documentation, use the following examples depending on the `doc_type`:

### Swift Package:
```bash
python3 DocumentationSync.py /path/to/package MyPackageTarget Package
```

### Xcode Project:
```bash
python3 DocumentationSync.py /path/to/xcodeproj MyProjectTarget xcodeproj --scheme_name MyScheme
```

### XCFramework:
```bash
python3 DocumentationSync.py /path/to/xcframework MyFrameworkTarget xcframework
```

## Third-Party Frameworks
[Pathlib](https://docs.python.org/3/library/pathlib.html)
[Typing](https://docs.python.org/3/library/typing.html)
[Requests](https://pypi.org/project/requests/)
[Markdown](https://python-markdown.github.io/)