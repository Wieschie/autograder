# Autograder
**Autograder** is a simple, configurable tool for grading programming assignments.

## Usage
### Command line
* `autograder init`: generates a `.config` directory with a skeleton `config.toml` file.
* `autograder testall`: runs tests defined in `config.toml` on all projects (any subdirectories not prefixed with a `.`)
* `autograder test DIRECTORIES`: runs tests on given list of directories

### Directory structure
The script looks for `.config` subdirectory, and will attempt to grade any subdirectories not prefixed with a `.`
```
working_directory
├── .config
    ├── config.toml
    ├── {necessary files}
├── {student_submissions}
```
### Configuration
* All tests are driven by the `config.toml` file.  [TOML](https://github.com/toml-lang/toml) is a simple configuration language designed to be human-friendly.
* An example configuration file can be found [here](autograder/.lib/config.toml).
* A full schema is defined in [config_schema.json](autograder/.lib/config_schema.json)
#### config.toml

| Key                   | Type    | Required | Notes                                                                                |
| ---                   | ----    | -------- | -----                                                                                |
| `output_dir`          | string  | **Yes**  | Name of directory in which to place all output files                                 |
| `nested_project`      | boolean | No       | used in the default Visual Studio project layout eg: "Project/Project/\*"            |
| [`[build]`](#build)   | object  | No       | Optional section containing build requirements                                       |
| [`[[test]]`](#tests)  | array   | **Yes**  | Array containing at least 1 test to run                                              |
| [`[output]`](#output) | object  | **Yes**  | Contains template information for logging output.                                    |
|                       |         |          |                                                                                      |

#### build
| Key              | Type  | Required | Notes                                                                                                                                                  |
| ---              | ----  | -------- | -----                                                                                                                                                  |
| `required_files` | array | No       | Array of `{file="str", dest="str"}` objects.  Files should be stored in `.config`, and can be copied anywhere within a project subdirectory as needed. |
| `commands`       | array | No       | Array of strings.  Commands to be executed in order for building the project.                                                                          |


#### Tests

#### JUnit
| Key         | Type   | Required | Notes     |
| ---         | ----   | -------- | -----     |
| `name`      | string | **Yes**  |           |
| `type`      | string | **Yes**  | `"junit"` |
| `classname` | string | **Yes**  | Filename of compiled classfile with JUnit test suite.  Should be paired with `required_files` in the build section to copy the classfile into each project directory. |

#### Diff
| Key                          | Type   | Required   | Notes                                                                         |
| ---                          | ----   | --------   | -----                                                                         |
| `name`                       | string | **Yes**    |                                                                               |
| `type`                       | string | **Yes**    | `"diff"`                                                                      |
| `points`                     | number | No         | All or nothing point value for test.                                          |
| `command`                    | string | **Yes**    |                                                                               |
| `stdin` **OR** `stdinFile`   | string | **Yes**    | Raw text, or name of text file, to feed to STDIN                              |
| `stdout` **OR** `stdoutFile` | string | **Yes** \* | Raw text, or name of text file, containing correct stdout to compare against. |
| `stderr` **OR** `stderrFile` | string | **Yes** \* | Raw text, or name of text file, containing correct stderr to compare against. |

\* Must have at least one of stdout and stderr defined

#### output
This section consists of [python template strings](https://docs.python.org/3.7/library/string.html#string.Template) used to format output.

| Key      | Type   | Required | Notes                                                               |
| ---      | ----   | -------- | -----                                                               |
| `build`  | string | **Yes**  | Used for each build command                                         |
| `junit`  | string | **Yes**  | Used for JUnit tests                                                |
| `diff`   | string | **Yes**  | Used for diff tests                                                 |
| `custom` | string | **Yes**  | Used for custom tests                                               |


## Development
1. Install Python 3.7, pip, and pipenv. 
2. Clone the repository
3. Run `pipenv sync --dev` to set up the virtual environment and install required packages.
