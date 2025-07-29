==================
Arc File Extractor
==================


.. image:: https://img.shields.io/pypi/v/arc_file_extractor.svg
        :target: https://pypi.python.org/pypi/arc_file_extractor

.. image:: https://readthedocs.org/projects/arc-file-extractor/badge/?version=latest
        :target: https://arc-file-extractor.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




A unified CLI for file extraction and compression on UNIX systems.

Features
--------

* **Simple extraction**: Extract files with a single command ``arc x file``
* **Easy compression**: Compress files and directories with ``arc c source``
* **Multiple formats**: Support for ZIP, TAR, GZIP, BZIP2, XZ, 7Z, and RAR formats
* **Dependency checking**: Built-in tool to check system dependencies
* **Rich output**: Beautiful colored output with file sizes and progress
* **Cross-platform**: Works on any UNIX-like system (Linux, macOS, BSD)

Installation
------------

Install Arc File Extractor using pip::

    pip install arc-file-extractor

Or install from source::

    git clone https://github.com/alves/arc_file_extractor.git
    cd arc_file_extractor
    pip install .

Usage
-----

Basic Commands
~~~~~~~~~~~~~~

**Extract a file:**

.. code-block:: bash

    arc x archive.zip
    arc x document.tar.gz
    arc x backup.7z

This will extract the file to a directory with the same name (without extension).

**Compress a file or directory:**

.. code-block:: bash

    arc c myfile.txt
    arc c mydirectory/
    arc c source/ -o backup.tar.gz

If no output file is specified, it defaults to creating a .zip file.

**List supported formats:**

.. code-block:: bash

    arc list

**Check system dependencies:**

.. code-block:: bash

    arc check

Advanced Usage
~~~~~~~~~~~~~~

**Verbose output:**

.. code-block:: bash

    arc x archive.zip -v
    arc c mydir/ -v

**Custom output file:**

.. code-block:: bash

    arc c myproject/ -o backup.tar.gz
    arc c documents/ -o docs_backup.7z

Supported Formats
~~~~~~~~~~~~~~~~~

**Extraction:**
- ZIP (.zip)
- TAR (.tar, .tar.gz, .tgz, .tar.bz2, .tbz, .tar.xz, .txz)
- GZIP (.gz)
- BZIP2 (.bz2)
- XZ (.xz)
- 7-Zip (.7z)
- RAR (.rar)

**Compression:**
- ZIP (.zip)
- TAR (.tar, .tar.gz, .tgz, .tar.bz2, .tbz, .tar.xz, .txz)
- 7-Zip (.7z)
- RAR (.rar)

Dependencies
~~~~~~~~~~~~

Arc File Extractor uses system tools for compression and extraction. Install the required tools:

**Ubuntu/Debian:**

.. code-block:: bash

    sudo apt install unzip tar gzip bzip2 xz-utils p7zip-full unrar zip

**Fedora/RHEL:**

.. code-block:: bash

    sudo dnf install unzip tar gzip bzip2 xz p7zip unrar zip

**Arch Linux:**

.. code-block:: bash

    sudo pacman -S unzip tar gzip bzip2 xz p7zip unrar zip

**macOS:**

.. code-block:: bash

    brew install p7zip unrar zip

Examples
--------

**Extract various archive types:**

.. code-block:: bash

    # Extract a ZIP file
    arc x project.zip
    # Creates: project/ directory

    # Extract a TAR.GZ file
    arc x backup.tar.gz
    # Creates: backup/ directory

    # Extract with verbose output
    arc x large_archive.7z -v

**Compress files and directories:**

.. code-block:: bash

    # Compress a directory to ZIP (default)
    arc c myproject/
    # Creates: myproject.zip

    # Compress to TAR.GZ
    arc c documents/ -o docs.tar.gz

    # Compress a single file
    arc c important_file.txt -o compressed.7z

**Check system status:**

.. code-block:: bash

    # Check what tools are installed
    arc check
    
    # List all supported formats
    arc list

Development
-----------

To set up for development::

    git clone https://github.com/alves/arc_file_extractor.git
    cd arc_file_extractor
    pip install -e .[dev]

Run tests::

    pytest

API Reference
-------------

Core Classes
~~~~~~~~~~~~

**ArcFileExtractor**

Main class for file extraction and compression operations.

.. code-block:: python

    from arc_file_extractor import ArcFileExtractor
    
    extractor = ArcFileExtractor()
    
    # Extract a file
    result = extractor.extract("archive.zip")
    
    # Compress a file/directory
    result = extractor.compress("source_dir", "output.tar.gz")

**Methods:**

- ``extract(file_path: str) -> int``: Extract a file to a directory with the same name
- ``compress(source_path: str, output_file: str = None) -> int``: Compress a file or directory

Utility Functions
~~~~~~~~~~~~~~~~~

**check_dependencies() -> List[str]**

Check if required external tools are installed. Returns a list of missing dependencies.

**get_supported_formats() -> dict**

Get supported file formats for extraction and compression.

**validate_file_path(file_path: str) -> bool**

Validate if a file path exists and is readable.

**get_file_size(file_path: str) -> str**

Get human-readable file size.

Contributing
------------

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
