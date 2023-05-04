# Documentation Builder

A Python module for building DocC Documentation archive files for Swift Packages, Xcode projects, or XCFrameworks.

## Installation

```python
from documentation_builder import DocumentationBuilder
```

## Example usage:
archive_path = DocumentationBuilder.build_documentation(repo_path, doc_type, target_name, scheme_name)

## Supported Documentation Types

### Swift Package:

```python
archive_path = DocumentationBuilder.build_documentation("/path/to/package", "Package", "MyPackageTarget")
```

### Xcode Project:

```python
archive_path = DocumentationBuilder.build_documentation("/path/to/xcodeproj", "xcodeproj", "MyProjectTarget", "MyScheme")
```

### XCFramework:

```python
archive_path = DocumentationBuilder.build_documentation("/path/to/xcframework", "xcframework", "MyFrameworkTarget")
```