# documentation_builder.py
import os
import subprocess
from pathlib import Path
from typing import Optional


class DocumentationBuilder:
    """
    A class for building DocC Documentation archive files.

    The class includes the following method:

    - build_documentation(directory_path: str, target_name: str) -> Optional[str]: 
    Determines the build route to use based on the files in the directory and builds the documentation archive.
    Currently only supports a single .xcodeproj or Package.swift.
    """

    @staticmethod
    def build_documentation(directory_path: str, target_name: str) -> Optional[str]:
        """
        Determines the build route to use based on the files in the directory and builds the documentation archive.
        Currently only supports a single .xcodeproj or Package.swift.

        Args:
            directory_path (str): The directory path containing the Swift package or Xcode project.
            target_name (str): The name of the target to build documentation for.
        
        Returns:
            Optional[str]: The .doccarchive file path, or None if an error occurred.
        """
        xcodeproj_path = None
        package_swift_path = None

        for entry in os.scandir(directory_path):
            if entry.is_file() and entry.name == "Package.swift":
                package_swift_path = entry.path
            elif entry.is_dir() and entry.name.endswith(".xcodeproj"):
                xcodeproj_path = entry.path

        if xcodeproj_path is not None:
            return DocumentationBuilder.__build_xcodeproj_documentation_archive(xcodeproj_path, target_name)
        elif package_swift_path is not None:
            return DocumentationBuilder.__build_package_documentation_archive(directory_path, target_name)
        else:
            print("Error: No valid .xcodeproj or Package.swift file found in the specified directory.")
            return None

    
    def __build_package_documentation_archive(package_file_path: str, package_name: str) -> Optional[str]:
        """
        Builds a Swift Package documentation archive using the https://github.com/apple/swift-docc-plugin package.
        
        Args:
            package_file_path (str): The file path of the Swift package.
            package_name (str): The name of the package to build documentation for.
        
        Returns:
            Optional[str]: The .doccarchive file path, or None if an error occurred.
        """
        # Create the 'docs' directory
        output_dir = "{package_file_path}/docs"
        os.makedirs(output_dir, exist_ok=True)

        try:
            # Execute the swift package command with the given arguments
            subprocess.run(
                [
                    "swift",
                    "package",
                    "--allow-writing-to-directory",
                    "./docs",
                    "generate-documentation",
                    "--target",
                    package_name,
                    "--disable-indexing",
                    "--output-path",
                    "./docs",
                    "--transform-for-static-hosting",
                    "--hosting-base-path",
                    package_name,
                ],
                check=True,
            )

        except subprocess.CalledProcessError as e:
            print(f"Error building documentation: {e}")
            print(
                "Please check that this DocC library is installed in order to create Swift Package Documentation: https://github.com/apple/swift-docc-plugin"
            )
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

    
    def __build_xcodeproj_documentation_archive(xcodeproj_file_path: str, scheme_name: str) -> Optional[str]:
        """
        Builds an Xcode project documentation archive using the xcodebuild command.
        
        Args:
            xcodeproj_file_path (str): The file path of the Xcode project.
            scheme_name (str): The name of the scheme to build documentation for.
        
        Returns:
            Optional[str]: The .doccarchive file path, or None if an error occurred.
        """

        # Create the 'docs' directory
        output_dir = f'{xcodeproj_file_path}/docs'
        os.makedirs(output_dir, exist_ok=True)  

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
            / "Debug-iphoneos"
            / f"{scheme_name}.doccarchive"
        )



        # Check if the .doccarchive file exists
        if docc_archive_path.exists():
            print(f"Documentation archive found at: {docc_archive_path}")
        else:
            print("Error: .doccarchive file not found")
            return None


        print("Finished building DocC Archive!")
        return docc_archive_path