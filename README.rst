|docbadge|

|buildbadge| |requirebadge| |pythonbadge| |licensebadge|

.. |docbadge| image:: https://readthedocs.org/projects/autograder/badge/?version=latest
     :target: https://autograder.readthedocs.io/en/latest/?badge=latest
     :alt: Documentation Status

.. |buildbadge| image:: https://ci.appveyor.com/api/projects/status/akwole9w6xp4l198/branch/master?svg=true
     :target: https://ci.appveyor.com/project/Wieschie/autograder/branch/master
     :alt: Build Status

.. |requirebadge| image:: https://requires.io/github/Wieschie/autograder/requirements.svg?branch=master
     :target: https://requires.io/github/Wieschie/autograder/requirements/?branch=master
     :alt: Requirements Status
     
.. |pythonbadge| image:: https://img.shields.io/badge/python-3.7-blue.svg
     :target: https://github.com/Wieschie/autograder/blob/master/Pipfile
     :alt: Python 3.7
     
.. |licensebadge| image:: https://img.shields.io/github/license/wieschie/autograder.svg
     :target: https://github.com/Wieschie/autograder/blob/master/LICENSE.txt
     :alt: MIT License

Click the docs badge above for full documentation!



Autograder
==========

.. begin_header

**Autograder** is a simple, configurable tool for grading programming
assignments.

.. begin_usage

Commands
--------

-  ``autograder init``: generates a ``.config`` directory with a
   skeleton ``config.toml`` file.
-  ``autograder testall``: runs tests defined in ``config.toml`` on all
   projects (any subdirectories not prefixed with a ``.``)
-  ``autograder test DIRECTORIES``: runs tests on given list of
   directories

.. end_usage

.. begin_dev

Development
-----------

Getting Set Up
~~~~~~~~~~~~~~

1. Install Python 3.7, pip, and pipenv.
2. Clone the repository
3. Run ``pipenv sync --dev`` to set up the virtual environment and
   install required packages.

Building
~~~~~~~~
This project can be built into a standalone application using PyInstaller.  
The repository contains several specfiles to do so.  Run ``pyinstaller 
<filename>.spec``, choosing the specfile based on the targeted platform and
style (onefile or onedir).
