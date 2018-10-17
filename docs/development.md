# Development Diary
## 2018-09-19
* Began to set up project in git.
* Use pipenv for dependency management
  * `pipenv install`: Install a dependency 
  * `pipenv install --dev`: Install as development dependency (not necessary for normal operation)
  * `pipenv shell`: Launch virtual python environment
* Use bumpversion for releases
  * `bumpversion --verbose --dry-run major/minor/fix`: See what increasing the version would actually do.
  * `.bumpversion.cfg`: contains all settings for bumpversion, including a list of places to increment the version
* Use sphinx for documentation
* pytest for testing
* [pyinstaller](https://www.pyinstaller.org/) to freeze?
* https://docs.python-guide.org/writing/documentation/
* https://docs.python-guide.org/writing/structure/

## 2018-09-25
* Set up Sphinx to work with markdown (and added this file).
  * `sphinx-build . _build`: can use `-b latex`
* Set path in `conf.py` to allow importing autograder module.  Will have to test this

## 2018-09-26
* Begin writing JUnit 5 tests for Complex numbers java project.  Will use to gather requirements + test running unit tests externally

## 2018-09-27
* Worked on running JUnit tests from command line.
  * `mkdir complex_numbers/out`
  * `javac -cp "lib/*:$COMP/src/" -d $COMP/out $COMP/src/p05/*`
  * `java -jar lib/junit-platform-console-standalone-1.3.1.jar -cp "$COMP/out/" -c p05.ComplexTests --reports-dir=$COMP/out`
* Look at [subprocess](https://docs.python.org/3/library/subprocess.html#module-subprocess) for managing external tooling
* Good resource for setting limits on spawned processes? https://stackoverflow.com/questions/47676469/creating-a-minimal-sandbox-for-running-binary-programs-in-python3

## 2018-10-02
* JUnit tests can be compiled against a single solution, then the class file used to test all projects.
  * Class file has to be copied into directory with other class files
  * This handles missing methods without erroring out
  
## 2018-10-04
* used `subprocess.Popen()` to run a command and save output
* Configured Sphinx to use Google-style docstrings and type hints
* https://pythonhosted.org/an_example_pypi_project/sphinx.html#full-code-example

## 2018-10-09
* `os.scandir()` lists subdirectories without recursing
* use `pathlib` to handle paths.  the `/` operator is overloaded to join paths
* Have to pass in `args` as a list to `subprocess` for POSIX compatibility. Use `shlex` to properly split strings into args
* JUnit timeouts work as expected.
* Use `difflib` to compare actual and expected output.  Only way to check if successful is returning an empty string?

## 2018-10-16
* begin writing sample TOML config file
* @TODO: implement 'secret' test files that are removed after test is complete

## 2018-10-17
* look at [python-anyconfig](https://github.com/ssato/python-anyconfig) to handle validation of toml file
* @TODO: implement wildcard substitution in config values
