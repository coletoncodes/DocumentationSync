# main.py
import sys
from utility import Utility
from ConfluenceUploader.config import Config
from ConfluenceUploader.confluence_uploader import ConfluenceUploader
from DocumentationBuilder.documentation_builder import DocumentationBuilder

# TODO: Let's initialize this and prompt the user for additional information instead. 
# We should add a setup for the different types of builds. Package, .xcodeproj, and .xcframeworks.
def main(repo_file_path: str, project_name: str, scheme_name: str):
    print(f'Step 1: Building DocC Archive')
    docc_archive = DocumentationBuilder.build_documentation(
        repo_file_path,
        project_name,
        scheme_name
    )

    # The following code is commented out and may be implemented in the future:
    # - Searching for CHANGELOG and README files in the repository
    # - Uploading README to the Library Parent Page
    # - (Potentially removed) Zipping the DocC Archive and uploading it to the Library Parent Page
    # - Uploading CHANGELOG to the Library CHANGELOG Page

    # print(
    #     f"Step 2: Searching for CHANGELOG and README file's in repo file path: {repo_file_path}")
    # changelog_file, readme_file = Utility.find_changelog_and_readme_files(
    #     repo_file_path
    # )

    # print(f"Step 3: Uploading README to Library Parent Page")
    # ConfluenceUploader.update_confluence_page(
    #     project_name,
    #     readme_file,
    #     Config.CONFLUENCE_PARENT_PAGE_ID
    # )

    # TODO: This will probably be removed, and updated to AWS page somehow
    # print(f"Step 4: Zip DocC Archive and upload to Library Parent Page")
    # docc_archive_zip = Utility.create_zip(docc_archive)
    # ConfluenceUploader.upload_file_to_confluence_page_as_attachment(
    #     docc_archive_zip,
    #     Config.CONFLUENCE_PARENT_PAGE_ID
    # )

    # print(f"Step 4: Uploading CHANGELOG to Library CHANGELOG Page")
    # ConfluenceUploader.update_confluence_page(
    #     f'{project_name} CHANGELOG',
    #     changelog_file,
    #     Config.CONFLUENCE_CHANGELOG_PAGE_ID
    # )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 DocumentationSync <repository_url> <project_name> <scheme_name>")
        sys.exit(1)

    repo_file_path = sys.argv[1]
    project_name = sys.argv[2]
    scheme_name = sys.argv[3]
    main(repo_file_path, project_name, scheme_name)
