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
  

.. rubric:: ``[build]``

*optional object*: Optional section containing build requirements
  

.. rubric:: ``[[test]]``

*array*: Array of test objects
  

.. rubric:: ``[output]``

*object*: Contains template information for logging output.

build
^^^^^


.. rubric:: ``required_files``

*optional array*: Array of ``{file="str", dest="str", secret=false}`` objects. Files should be 
stored in .config, and can be copied anywhere within a project subdirectory as needed. 

.. note:: 
  ``secret`` is optional; set to true if you want the files to be removed after the tests have run. This could
  be useful if students have access to the folders being graded (such as on a networked drive).

  

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


.. rubric:: ``glob_command``

*boolean*: Use `bash-style globbing <http://tldp.org/LDP/abs/html/globbingref.html>`__
to resolve the executable name.

.. note::
  Useful when executables follow a common naming format but have unique names 
  (``CS255P01<LastName>.exe`` would be matched by ``CS225P01*.exe``).

  Arguments can still be used with globbed commands, but only the executable name
  itself will be resolved.


.. rubric:: ``stdin`` **OR** ``stdinFile``

*string*: Raw text, or name of text file, to feed to STDIN.


.. rubric:: ``stdout`` **OR** ``stdoutFile``

*string*: Raw text, or name of text file, containing correct STDOUT compare against.


.. rubric:: ``stderr`` **OR** ``stderrFile``

*string*: Raw text, or name of text file, containing correct STDERR to compare against.

\* Must have at least one of stdout and stderr defined


Custom
######

.. rubric:: ``command``

*string*: command to execute.  Output will be captured.


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
