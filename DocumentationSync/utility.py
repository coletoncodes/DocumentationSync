# utility.py

import markdown
import shutil
import os
import sys


class Utility:
    """
A utility class containing methods for working with files and Markdown content.

The class includes the following methods:

- render_markdown_content_as_HTML(content: str) -> str: Renders a Markdown content string as HTML, 
escaping & characters.

- create_zip(file_path: str) -> str: Creates a zip archive from a specified file path and returns the zipped 
file's destination.

- find_changelog_and_readme_files(repo_file_path: str) -> tuple[str, str]: Finds the changelog and readme files
 in a given repository directory and returns a tuple containing their paths.

"""

    @staticmethod
    def render_markdown_file_as_HTML(markdown_file_path: str) -> str:
        """
        Renders a Markdown file content as HTML, escaping `&` characters.

        :param content: The Markdown file path string to be rendered as HTML.
        :return: The rendered HTML content.
        """
        with open(markdown_file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            markdown_content = markdown.markdown(file_content, output_format='xhtml')
            return markdown_content.replace('&', '&amp;')


    @staticmethod
    def create_zip(file_path: str) -> str:
        """
        Creates a zip archive from a specified file path.

        :param file_path: The path to the file to be zipped.
        :return: The zipped file's destination path.
        """
        root_path, _ = os.path.splitext(file_path)
        print(
            f"Attempting to create .zip archive for root: {root_path}, from file path: {file_path}")
        return shutil.make_archive(root_path, 'zip', file_path)


    @staticmethod
    def find_changelog_and_readme_files(repo_file_path: str) -> tuple[str, str]:
        """
        Finds the changelog and readme files in a given repository directory.

        :param repo_file_path: The path to the repository directory.
        :return: A tuple containing the paths to the changelog and readme files, respectively.
        :raises SystemExit: If either the changelog or readme file is not found in the repository directory.
        """
        changelog_file = None
        readme_file = None

        files = os.listdir(repo_file_path)

        for file in files:
            file_lower = file.lower()
            if file_lower == 'changelog.md':
                changelog_file = os.path.join(repo_file_path, file)
            elif file_lower == 'readme.md':
                readme_file = os.path.join(repo_file_path, file)

            if changelog_file and readme_file:
                break

        if not changelog_file:
            print('changelog.md file not found in the repository',
                    file=sys.stderr)
            sys.exit(1)

        if not readme_file:
            print('readme.md file not found in the repository',
                    file=sys.stderr)
            sys.exit(1)

        print(f'Found changelog and readme files.')
        return changelog_file, readme_file