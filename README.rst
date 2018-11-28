|docbadge| |requirebadge|

.. |docbadge| image:: https://readthedocs.org/projects/autograder/badge/?version=latest
     :target: https://autograder.readthedocs.io/en/latest/?badge=latest
     :alt: Documentation Status

.. |requirebadge| image:: https://requires.io/github/Wieschie/autograder/requirements.svg?branch=master
     :target: https://requires.io/github/Wieschie/autograder/requirements/?branch=master
     :alt: Requirements Status

.. begin_usage

Autograder
==========


**Autograder** is a simple, configurable tool for grading programming
assignments.

Usage
-----

Commands
~~~~~~~~~~~~

-  ``autograder init``: generates a ``.config`` directory with a
   skeleton ``config.toml`` file.
-  ``autograder testall``: runs tests defined in ``config.toml`` on all
   projects (any subdirectories not prefixed with a ``.``)
-  ``autograder test DIRECTORIES``: runs tests on given list of
   directories



Directory structure
~~~~~~~~~~~~~~~~~~~

The script looks for ``.config`` subdirectory, and will attempt to grade
any subdirectories not prefixed with a ``.``

::

   working_directory
   ├── .config
       ├── config.toml
       ├── {necessary files}
   ├── {student_submissions}

Workflow
~~~~~~~~

1. Gather all student submissions in a common directory, such that each submission is a subdirectory.
#. Run ``autograder init`` to generate a ``.config/`` directory.
#. Edit ``.config/config.toml`` as necessary to define environment and tests (see :doc:`Configuration</configuration>` for more details.
#. Use ``autograder testall`` to run defined tests against all projects.
#. Results with be collected in the ``.results/`` directory.

.. end_usage

Configuration
~~~~~~~~~~~~~

-  All tests are driven by the ``config.toml`` file.
   `TOML <https://github.com/toml-lang/toml>`__ is a simple
   configuration language designed to be human-friendly.
-  A full schema is defined in
   `config_schema.json <https://github.com/Wieschie/autograder/blob/master/autograder/.lib/config_schema.json>`__


config.toml
^^^^^^^^^^^


.. rubric:: ``output_dir``

*string*: Name of directory in which to place all output files
  

.. rubric:: ``nested_project``

*optional boolean*: Set to true if projects follow the default Visual Studio layout eg: ``Project/Project/*``.

.. note::
  This sets the working directory to the inner project directory.  This means you can run 
  commands and copy files without worrying about the project name.
  

.. rubric:: ``[build]``

*optional object*: Optional section containing build requirements
  

.. rubric:: ``[[test]]``

*array*: Array of test objects
  

.. rubric:: ``[output]``

*object*: Contains template information for logging output.

build
^^^^^


.. rubric:: ``required_files``

*optional array*: Array of ``{file="str", dest="str"}`` objects. Files should be 
stored in .config, and can be copied anywhere within a project subdirectory as needed.
  

.. rubric:: ``commands``

*optional array*: Array of strings. Commands to be executed in order for building the project.

Tests
^^^^^
All tests share some common configuration values:


.. rubric:: ``name``

*string*: Display name of test used when logging results.


.. rubric:: ``type``

*string*: Defines the type of test to run.  Can be ``"junit", "diff", "custom"``


JUnit
#####
.. note::
  You can attach point values to invidual JUnit tests.  To do so, use an annotation on 
  the test function: ``@DisplayName("<Name here>points:10")``.  Points can be any floating
  point value.

.. rubric:: ``classname``

*string*: Filename of compiled classfile with JUnit test suite. Should be paired with 
``required_files`` in the build section to copy the classfile into each project directory.


Diff
####

.. rubric:: ``points``

*number*: All or nothing point value for test.


.. rubric:: ``command``

*string*: command to execute.  Output will be captured and compared.


.. rubric:: ``stdin`` **OR** ``stdinFile``

*string*: Raw text, or name of text file, to feed to STDIN.


.. rubric:: ``stdout`` **OR** ``stdoutFile``

*string*: Raw text, or name of text file, containing correct STDOUT compare against.


.. rubric:: ``stderr`` **OR** ``stderrFile``

*string*: Raw text, or name of text file, containing correct STDERR to compare against.

\* Must have at least one of stdout and stderr defined


output
^^^^^^

This section consists of `python template
strings <https://docs.python.org/3.7/library/string.html#string.Template>`__
used to format output.

.. note::
  The valid identifiers are ``$name, $cmd, $retval, $stdout, $stderr, $points, $diffout``.
  Any identifiers that do not pertain to the current test will be replaced with an empty string.


.. rubric:: ``build``

*string*: Used for each build command


.. rubric:: ``junit``

*string*: Used for JUnit tests


.. rubric:: ``diff``

*string*: Used for diff tests


.. rubric:: ``custom``

*string*: Used for custom tests

.. end_config

Development
-----------

1. Install Python 3.7, pip, and pipenv.
2. Clone the repository
3. Run ``pipenv sync --dev`` to set up the virtual environment and
   install required packages.
