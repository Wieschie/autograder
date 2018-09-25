# Development Diary
## 2018-09-19
* Began to set up project in git.
* Use pipenv for dependency management
  * ``pipenv install``: Install a dependency 
  * ``pipenv install --dev``: Install as development dependency (not necessary for normal operation)
  * ``pipenv shell``: Launch virtual python environment
* Use bumpversion for releases
  * ``bumpversion --verbose --dry-run major/minor/fix``: See what increasing the version would actually do.
  * ``.bumpversion.cfg``: contains all settings for bumpversion, including a list of places to increment the version
* Use sphinx for documentation
  * http://www.sphinx-doc.org/en/master/usage/quickstart.html
* pytest for testing
* pyinstaller to freeze? https://www.pyinstaller.org/
https://docs.python-guide.org/writing/documentation/
https://docs.python-guide.org/writing/structure/

## 2018-09-25
* Set up Sphinx to work with markdown (and added this file).
  * ``sphinx-build . _build``: can use `-b latex`
* Set path in `conf.py` to allow importing autograder module.  Will have to test this

