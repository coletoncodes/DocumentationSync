# documentation_builder.py
import os
import subprocess
from pathlib import Path
from typing import Optional


class DocumentationBuilder:
    """
    A class for building DocC Documentation archive files.

    The class includes the following method:

    - build_documentation_archive(repo_path: str, doc_type: str, target_name: str, scheme_name: Optional[str]) -> Optional[str]: 
    Determines the build route to use based on the documentation type and builds the documentation archive.
    Supports Package.swift, .xcodeproj, or .xcframework.
    """

    @staticmethod
    def build_documentation_archive(
        repo_path: str, 
        doc_type: str, 
        target_name: str, 
        scheme_name: Optional[str] = None
        ) -> Optional[str]:
        """
        Determines the build route to use based on the documentation type and builds the documentation archive.
        Supports Package.swift, .xcodeproj, or .xcframework.

        For Packages and .xcframeworks make sure this [Apple DocC Library](https://github.com/apple/swift-docc-plugin) is installed.

        Args:
            repo_path (str): The path to the repository containing the Swift package, Xcode project, or XCFramework.
            doc_type (str): The type of documentation to build, either "Package", "xcodeproj", or "xcframework".
            target_name (str): The name of the target to build documentation for.
            scheme_name (Optional[str]): The name of the scheme to build during documentation creation. Required for .xcodeproj type.

        Returns:
            Optional[str]: The .doccarchive file path, or None if an error occurred.
        """

        # Create output directory
        output_dir = DocumentationBuilder.__create_docs_directory(repo_path)

        # Build documentation based on doc_type
        if doc_type == "Package":
            package_swift_path = DocumentationBuilder.__find_package_path(
                repo_path)
            if package_swift_path:
                return DocumentationBuilder.__build_package_documentation_archive(
                    package_swift_path,
                    target_name,
                    output_dir
                    )
        elif doc_type == "xcodeproj":
            xcodeproj_path = DocumentationBuilder.__find_xcodeproj_path(
                repo_path,
                output_dir
                )
            if xcodeproj_path and scheme_name:
                return DocumentationBuilder.__build_xcodeproj_documentation_archive(
                    xcodeproj_path,
                    target_name, 
                    scheme_name,
                    output_dir
                    )
        elif doc_type == "xcframework":
            xcframework_path = DocumentationBuilder.__find_xcframework_path(
                repo_path,
                output_dir
                )
            if xcframework_path:
                return DocumentationBuilder.__build_xcframework_documentation_archive(
                    xcframework_path,
                    target_name,
                    output_dir
                    )
        else:
            supported_doc_types = ["Package", "xcodeproj", "xcframework"]
            print(f"Error: Invalid documentation type specified. Supported types are: {', '.join(supported_doc_types)}")
            return None

    @staticmethod
    def __find_package_path(directory_path: str) -> Optional[str]:
        for entry in os.scandir(directory_path):
            if entry.is_file() and entry.name == "Package.swift":
                return os.path.dirname(entry.path)
        return None
    
    @staticmethod
    def __find_path_with_extension(directory_path: str, extension: str) -> Optional[str]:
        for entry in os.scandir(directory_path):
            if entry.is_dir() and entry.name.endswith(extension):
                return entry.path
        return None

    @staticmethod
    def __find_xcodeproj_path(directory_path: str) -> Optional[str]:
        return DocumentationBuilder.__find_path_with_extension(directory_path, ".xcodeproj")

    @staticmethod
    def __find_xcframework_path(directory_path: str) -> Optional[str]:
        return DocumentationBuilder.__find_path_with_extension(directory_path, ".xcframework")

    @staticmethod
    def __create_docs_directory(base_path: str) -> str:
        output_dir = f'{base_path}/docs'
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    def __build_package_documentation_archive(
        package_file_path: str, 
        package_name: str, 
        output_dir: str
        ) -> Optional[str]:
        """

        Args:
            package_file_path (str): The file path of the Swift package.
            package_name (str): The name of the package to build documentation for.
            output_dir (str): The output directory to store the archive.

        Returns:
            Optional[str]: The .doccarchive file path, or None if an error occurred.
        """

        try:
            # Execute the swift package command with the given arguments
            subprocess.run(
                [
                    "swift",
                    "package",
                    "--allow-writing-to-directory",
                    output_dir,
                    "generate-documentation",
                    "--target",
                    package_name,
                    "--disable-indexing",
                    "--output-path",
                    output_dir,
                    "--transform-for-static-hosting",
                    "--hosting-base-path",
                    package_name
                ],
                check=True,
                cwd=package_file_path
            )

        except subprocess.CalledProcessError as e:
            print(f"Error building documentation: {e}")
            return None

        docc_archive_path = (
            Path(package_file_path)
            / ".build"
            / "plugins"
            / "Swift-DocC"
            / "outputs"
            / f"{package_name}.doccarchive"
        )

        if not docc_archive_path.exists():
            print("Error: .doccarchive file not found")
            return None

        print("Finished building DocC Archive!")
        return docc_archive_path

    def __build_xcodeproj_documentation_archive(
        xcodeproj_file_path: str, 
        project_name: str, 
        scheme_name: str, 
        output_dir: str
        ) -> Optional[str]:
        """
        Builds an Xcode project documentation archive using the xcodebuild command.

        Args:
            xcodeproj_file_path (str): The file path of the Xcode project.
            project_name (str): The name of the project. Will be used to find the project_name.doccarchive
            scheme_name: (str): The name of the scheme to build documentation for.
            output_dir (str): The output directory to store the archive.

        Returns:
            Optional[str]: The .doccarchive file path, or None if an error occurred.
        """

        # Execute the xcodebuild command with the docbuild action and output path
        try:
            subprocess.run(
                [
                    "xcodebuild",
                    "-project",
                    xcodeproj_file_path,
                    "-scheme",
                    scheme_name,
                    "docbuild",
                    "-derivedDataPath",
                    output_dir
                ],
                check=True,
            )

        except subprocess.CalledProcessError as e:
            print(f"Error building documentation: {e}")
            return None

        # Define the path to the .doccarchive file
        docc_archive_path = (
            Path(output_dir)
            / "Build"
            / "Products"
            / f'{scheme_name}-iphoneos'
            / f"{project_name}.doccarchive"
        )

        # Check if the .doccarchive file exists
        if docc_archive_path.exists():
            print(f"Documentation archive found at: {docc_archive_path}")
        else:
            print("Error: .doccarchive file not found")
            return None

        print("Finished building DocC Archive!")
        return docc_archive_path
    

    @staticmethod
    def __build_xcframework_documentation_archive(
        xcframework_file_path: str, 
        framework_name: str, 
        output_dir: str
        ) -> Optional[str]:
        """
        Builds an .xcframework documentation archive using the Apple-DocC plugin.

        Args:
            xcframework_file_path (str): The file path of the .xcframework.
            framework_name (str): The name of the framework to build documentation for.
            output_dir (str): The output directory to store the archive.

        Returns:
            Optional[str]: The .doccarchive file path, or None if an error occurred.
        """

        try:
            # Execute the xcodebuild command with the docbuild action and output path
            subprocess.run(
                [
                    "xcodebuild",
                    "docbuild",
                    "-xcframework",
                    xcframework_file_path,
                    "-derivedDataPath",
                    output_dir
                ],
                check=True,
            )

        except subprocess.CalledProcessError as e:
            print(f"Error building documentation: {e}")
            return None

        # Define the path to the .doccarchive file
        docc_archive_path = Path(output_dir) / f"{framework_name}.doccarchive"

        # Check if the .doccarchive file exists
        if docc_archive_path.exists():
            print(f"Documentation archive found at: {docc_archive_path}")
        else:
            print("Error: .doccarchive file not found")
            return None

        print("Finished building DocC Archive!")
        return docc_archive_path
