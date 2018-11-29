Development Diary
=================

2018-09-19
----------

-  Began to set up project in git.
-  Use pipenv for dependency management

   -  ``pipenv install``: Install a dependency
   -  ``pipenv install --dev``: Install as development dependency (not
      necessary for normal operation)
   -  ``pipenv shell``: Launch virtual python environment

-  Use bumpversion for releases

   -  ``bumpversion --verbose --dry-run major/minor/fix``: See what
      increasing the version would actually do.
   -  ``.bumpversion.cfg``: contains all settings for bumpversion,
      including a list of places to increment the version

-  Use sphinx for documentation
-  pytest for testing
-  `pyinstaller <https://www.pyinstaller.org/>`__ to freeze?
-  https://docs.python-guide.org/writing/documentation/
-  https://docs.python-guide.org/writing/structure/


2018-09-25
----------

-  Set up Sphinx to work with markdown (and added this file).

   -  ``sphinx-build . _build``: can use ``-b latex``

-  Set path in ``conf.py`` to allow importing autograder module. Will
   have to test this


2018-09-26
----------

-  Begin writing JUnit 5 tests for Complex numbers java project. Will
   use to gather requirements + test running unit tests externally


2018-09-27
----------

-  Worked on running JUnit tests from command line.

   -  ``mkdir complex_numbers/out``
   -  ``javac -cp "lib/*:$COMP/src/" -d $COMP/out $COMP/src/p05/*``
   -  ``java -jar lib/junit-platform-console-standalone-1.3.1.jar -cp "$COMP/out/" -c p05.ComplexTests --reports-dir=$COMP/out``

-  Look at
   `subprocess <https://docs.python.org/3/library/subprocess.html#module-subprocess>`__
   for managing external tooling
-  Good resource for setting limits on spawned processes?
   https://stackoverflow.com/questions/47676469/creating-a-minimal-sandbox-for-running-binary-programs-in-python3


2018-10-02
----------

-  JUnit tests can be compiled against a single solution, then the class
   file used to test all projects.

   -  Class file has to be copied into directory with other class files
   -  This handles missing methods without erroring out


2018-10-04
----------

-  used ``subprocess.Popen()`` to run a command and save output
-  Configured Sphinx to use Google-style docstrings and type hints
-  https://pythonhosted.org/an_example_pypi_project/sphinx.html#full-code-example


2018-10-09
----------

-  ``os.scandir()`` lists subdirectories without recursing
-  use ``pathlib`` to handle paths. the ``/`` operator is overloaded to
   join paths
-  Have to pass in ``args`` as a list to ``subprocess`` for POSIX
   compatibility. Use ``shlex`` to properly split strings into args
-  JUnit timeouts work as expected.
-  Use ``difflib`` to compare actual and expected output. Only way to
   check if successful is returning an empty string?


2018-10-16
----------

-  begin writing sample TOML config file
-  implement ‘secret’ test files that are removed after test is complete


2018-10-17
----------

-  look at
   `python-anyconfig <https://github.com/ssato/python-anyconfig>`__ to
   handle validation of toml file


2018-10-18
----------

-  Rewrote config class to act as a shim for config dictionary

   -  goal here is to seamlessly handle substitution of placeholder
      values
   -  Not sure if those placeholders are even necessary - can’t
      everything be handled by using relative paths from working
      directory?

-  wrote JSON schema for config file
-  Limiting resource usage is not trivial in any cross-platform manner

   -  currently need to use JobObjects on Windows:
      https://github.com/giampaolo/psutil/issues/1149

      -  https://mail.python.org/pipermail/python-ideas/2017-October/047473.html

   -  can use rlimits for Unix processes:
      https://docs.python.org/3/library/resource.html
   -  https://github.com/Submitty/Submitty/blob/master/grading/default_config.h

-  Using @DisplayName to export point values for individual JUnit tests
   to log:

   -  Next step is parsing JUnit logs


2018-10-22
----------

-  ``junit.py`` parses both junit xml files and extracts point values


2018-10-23
----------

-  Not sure about creating docx files: options are docx-mailmerge and
   docxtpl

   -  just add an option to export results in csv to allow a mail merge
      later?

-  Write ``TestResult`` to handle tests instead of logging directly
-  Handle point values in Results
-  Handle parsed JUnit results


2018-10-24
----------

-  dump results in human readable txt


2018-10-25
----------

-  current plan: assign main process to Win32 JobObject

   -  set limits before spawning test processes (maybe set some limits
      before building?)


2018-10-28
----------

-  For limiting file usage on windows: can’t seem to limit open file
   handles.

   -  try setting a notification limit on bytes read / wrote, then kill
      process if it increments?


2018-10-30
----------

-  JobObjects work well when associating the parent script with a single
   job

   -  Complicates limiting the number of active processes. Should be
      able to set the limit to the configured value + 1 (script is
      included in the job)
   -  Java processes spawn at least one additional thread for the
      garbage collector on linux

-  @TODO RLIMIT_NPROC applies to the user that owns the process, not
   just the process. for this to work, script must be run as a separate
   user.


2018-11-11
----------

-  Add third job type, or add pre/post jobs (but then have to figure out
   how to redirect output?)


2018-11-13
----------

-  DONE: Use Template strings and
   `substitute() <https://docs.python.org/3/library/string.html#template-strings>`__
   for templating output
-  DONE: take stdin from file for diff tests
-  @TODO: schema docs: make an issue / look at writing a pull request?
   “sphinx-jsonschema extends JSON Schema with the $$target key. This
   key is only recognized at the outermost object of the schema.”


2018-11-21
----------

-  DONE: compare stderr
-  DONE: save all results to one directory


2018-11-24
----------

-  Handle Visual Studio projects with ``nested_project`` config value.

   -  Just attempts to change to ``project/project`` when given
      directory ``project``.

2018-11-27
----------

- How to handle custom tests?  run command and pipe output to second command?
- TODO: split README into more rst files for better use on sphinx

2018-11-29
----------

- sum points total in results
