Usage
=====

.. include:: ../README.rst
             :start-after: begin_usage
             :end-before: end_usage

             
Directory structure
-------------------

The script looks for ``.config`` subdirectory, and will attempt to grade
any subdirectories not prefixed with a ``.``

::

   working_directory
   ├── .config
       ├── config.toml
       ├── {necessary files}
   ├── {student_submissions}

Workflow
--------

1. Gather all student submissions in a common directory, such that each submission is a subdirectory.
#. Run ``autograder init`` to generate a ``.config/`` directory.
#. Edit ``.config/config.toml`` as necessary to define environment and tests (see :doc:`Configuration</configuration>` for more details.
#. Use ``autograder testall`` to run defined tests against all projects.
#. Results with be collected in the ``.results/`` directory.