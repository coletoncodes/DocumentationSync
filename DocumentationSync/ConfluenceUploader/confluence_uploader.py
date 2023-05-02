import json
import requests
from requests.auth import HTTPBasicAuth
from .config import Config
from utility import Utility


class ConfluenceUploader:
    """
    A class for uploading files and updating Confluence pages.

    This class uses the Confluence REST API and requires the following configuration values to be set:
    - `CONFLUENCE_EMAIL`: The email address of the Confluence account to use for authentication.
    - `CONFLUENCE_API_KEY`: The API key of the Confluence account to use for authentication.
    - `CONFLUENCE_BASE_URL`: The base URL of the Confluence instance to use.
    - `CONFLUENCE_SPACE_KEY`: The key of the Confluence space to use.

    These values should be set in a separate `config.py` module, which should be placed in the same directory as the script that uses the `ConfluenceUploader` class.
    
    The class includes the following methods:

    - update_confluence_page(title: str, markdown_file: str, page_id: str): 
    This function updates a Confluence page based on it's page_id with the given title and markdown file.

    - upload_file_to_confluence_page_as_attachment(zip_file: str, page_id: str):
    This function uploads a zip_file to a specified Confluence page as an attachment.
    """

    AUTH = HTTPBasicAuth(
        Config.CONFLUENCE_EMAIL,
        Config.CONFLUENCE_API_KEY
    )

    HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }


    @staticmethod
    def update_confluence_page(title: str, markdown_file: str, page_id: str):
        """
        This function updates a Confluence page with the given title and markdown style content.

        :param title: The title of the Confluence page to be updated.
        :type title: str
        :param markdown_file: The markdown content to be added to the Confluence page.
        :type markdown_file: str
        :param page_id: The ID of the Confluence page to be updated.
        :type page_id: str

        :returns: None
        """
        # Get the current version number of the page, which is required by the Confluence API for updates.
        current_version = ConfluenceUploader.__get_page_version(page_id)
        url = f'{Config.CONFLUENCE_BASE_URL}/pages/{page_id}'

        # Render the Markdown File as HTML.
        body_content = Utility.render_markdown_file_as_HTML(
            markdown_file
        )

        # Create the payload for the update request with the new version number and content.
        payload = json.dumps({
            "id": page_id,
            "status": "current",
            "title": title,
            "spaceId": Config.CONFLUENCE_SPACE_KEY,
            "body": {
                "representation": "storage",
                "value": body_content
            },
            "version": {
                "number": current_version + 1,
                "message": "Automation Update"
            }
        })

        # Send a PUT request to the Confluence API to update the page.
        response = requests.put(
            url=url,
            data=payload,
            headers=ConfluenceUploader.HEADERS,
            auth=ConfluenceUploader.AUTH
        )

        # Raise an exception if the request fails.
        response.raise_for_status()
        print("Finished uploading content to confluence")

    @staticmethod
    def upload_file_to_confluence_page_as_attachment(zip_file: str, page_id: str):
        """
        This function uploads a file to a specified Confluence page as an attachment.

        :param zip_file: The file to be uploaded
        :type zip_file: str
        :param page_id: The Confluence page id where the file will be uploaded as an attachment
        :type page_id: str
        :return: None
        :rtype: None
        """
        files = {'file': open(zip_file, 'rb')}
        headers = {
            'X-Atlassian-Token': 'no-check'
        }
        params = {
            'minorEdits': 'false'
        }

        url = f'{Config.CONFLUENCE_BASE_URL}/content/{page_id}/child/attachment'
        print(f'Attempting to upload {zip_file} to {url}')

        response = requests.put(
            url,
            auth=ConfluenceUploader.AUTH,
            files=files,
            headers=headers,
            params=params
        )

        response.raise_for_status()
        print("Finished uploading Attachment to Confluence Page!")


    def __get_page_version(page_id: str) -> int:
        """
        This function takes a page_id as input and returns the current version number of the page.
        This is used to increment the page version for every update, which is required by Confluence API.

        Parameters:
        page_id (str): The Confluence page id of the page to retrieve the version number for.

        Returns:
        int: The current version number of the Confluence page.

        Raises:
        requests.exceptions.HTTPError: If the GET request to retrieve the page data from the Confluence API fails.
        """
        # Send a GET request to the Confluence API to get the page data.
        response = requests.get(
            f'{Config.CONFLUENCE_BASE_URL}/pages/{page_id}',
            auth=ConfluenceUploader.AUTH,
            headers=ConfluenceUploader.HEADERS
        )
        # Raise an exception if the request fails.
        response.raise_for_status()
        # Parse the JSON response.
        page_data = response.json()
        # Return the version number of the page.
        return page_data['version']['number']
