# DocumentationSync
A python library that uploads internal library documentation to confluence.

## Tech Lead/Owner
Coleton Gorecke, cgorecke@firstorion.com

## Purpose
This library helps sync the README.md, Changelog.md, and .doccarchive files for internal libraries with their respective page in Confluence. 

## Requirements
Python 3.5 or greater

## Dependencies
- pathlib: introduced in Python 3.4
- typing: introduced in Python 3.5
- requests: version 2.0.0 or higher should work with Python 3.5.
- markdown: version 3.0.0 or higher should work with Python 3.5.

## Installation
If applicable, provide instructions on how to install the library if it's not a SPM, including any necessary steps to set up the environment.

## External Tools
This library requires some setup from Confluence and should be configured in the ConfluenceUploader/config.py. 

Example: 'https://privacystar.atlassian.net/wiki/api/v2'
- CONFLUENCE_BASE_URL = 'your-base-url'
Example: 'cgorecke@firstorion.com
- CONFLUENCE_EMAIL = 'your-email'
Example: 'ATATT....'
- CONFLUENCE_API_KEY = 'your-api-key'
Example: This is the mobile eng space id: '800260186'. 
- CONFLUENCE_SPACE_KEY = 'confluence-space-key'
Found in URL of page. 
Example: your-base-url/wiki/spaces/Space_name/pages/Parent_Page_ID/Page_Name
- CONFLUENCE_PARENT_PAGE_ID = 'parent-page-id'
Found in URL of page. 
Example: your-base-url/wiki/spaces/Space_name/pages/Changelog_Page_ID/Page_Name
- CONFLUENCE_CHANGELOG_PAGE_ID = 'changelog-id'

[Manage Confluence API Keys](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)

## Third-Party Frameworks
[Pathlib](https://docs.python.org/3/library/pathlib.html)
[Typing](https://docs.python.org/3/library/typing.html)
[Requests](https://pypi.org/project/requests/)
[Markdown](https://python-markdown.github.io/)