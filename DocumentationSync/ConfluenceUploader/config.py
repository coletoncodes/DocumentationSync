# config.py

# Provides the configuration needed for this script package.
class Config:
    # Example: 'https://privacystar.atlassian.net/wiki/api/v2'
    CONFLUENCE_BASE_URL = 'your-base-url'
    # Example: 'cgorecke@firstorion.com
    CONFLUENCE_EMAIL = 'your-email'
    # Example: 'ATATT....'
    CONFLUENCE_API_KEY = 'your-api-key'
    # Example: This is the mobile eng space id: '800260186'. 
    CONFLUENCE_SPACE_KEY = 'confluence-space-key'
    # Found in URL of page. 
    # Example: your-base-url/wiki/spaces/Space_name/pages/Parent_Page_ID/Page_Name
    CONFLUENCE_PARENT_PAGE_ID = 'parent-page-id'
    # Found in URL of page. 
    # Example: your-base-url/wiki/spaces/Space_name/pages/Changelog_Page_ID/Page_Name
    CONFLUENCE_CHANGELOG_PAGE_ID = 'changelog-id'
