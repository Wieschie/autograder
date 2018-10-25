# Autograder
**Autograder** is a simple, configurable tool for grading programming assignments.

## Usage
### Directory structure
```
project_directory
├── .config
    ├── config.toml
    ├── {necessary files}
├── {student_submissions}
```
### Configuration
* All tests are driven by the `config.toml` file.  [TOML](https://github.com/toml-lang/toml) is a simple configuration language designed to be human-friendly.
* An example configuration file can be found [here](autograder/config.toml).
* A full schema is defined in [config_schema.json](autograder/config_schema.json)

## Development
1. Install Python 3.7, pip, and pipenv. 
2. Clone the repository
3. Run `pipenv sync --dev` to set up the virtual environment and install required packages.
