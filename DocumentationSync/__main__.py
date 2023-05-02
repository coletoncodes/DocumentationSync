# main.py
import sys
from utility import Utility
from ConfluenceUploader.config import Config
from ConfluenceUploader.confluence_uploader import ConfluenceUploader
from DocumentationBuilder.documentation_builder import DocumentationBuilder

# TODO: User should specify framework type in init.
def main(repo_file_path: str, project_name: str):
    print(f'Step 1: Building DocC Archive')
    docc_archive = DocumentationBuilder.build_documentation(
        repo_file_path,
        project_name
    )

    print(
        f"Step 2: Searching for CHANGELOG and README file's in repo file path: {repo_file_path}")
    changelog_file, readme_file = Utility.find_changelog_and_readme_files(
        repo_file_path
    )

    print(f"Step 3: Uploading README to Library Parent Page")
    ConfluenceUploader.update_confluence_page(
        project_name,
        readme_file,
        Config.CONFLUENCE_PARENT_PAGE_ID
    )

    # TODO: This will probably be removed, and updated to AWS page somehow
    print(f"Step 4: Zip DocC Archive and upload to Library Parent Page")
    docc_archive_zip = Utility.create_zip(docc_archive)
    ConfluenceUploader.upload_file_to_confluence_page_as_attachment(
        docc_archive_zip,
        Config.CONFLUENCE_PARENT_PAGE_ID
    )

    print(f"Step 4: Uploading CHANGELOG to Library CHANGELOG Page")
    ConfluenceUploader.update_confluence_page(
        f'{project_name} CHANGELOG',
        changelog_file,
        Config.CONFLUENCE_CHANGELOG_PAGE_ID
    )

    print("All Steps Completed!")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 DocumentationSync <repository_url> <project_name>")
        sys.exit(1)

    repo_file_path = sys.argv[1]
    project_name = sys.argv[2]
    main(repo_file_path, project_name)
