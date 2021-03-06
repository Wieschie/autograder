import sys
import time

import numpy
import os
import subprocess
import win32api

__job = None


def win32_limit(max_memory: int = None, max_processes: int = None):
    """
    Sets per-process limits on Windows systems.

    WARNING: Currently creates a single job, so affects all spawned processes.
    """
    # check if script has already been added to the job
    # TODO check if necessary
    global __job
    # if IsProcessInJob(GetCurrentProcess(), __job):
    if __job:
        return

    __job = win32api.CreateJobObject(None, "")
    win32api.AssignProcessToJobObject(__job, win32api.GetCurrentProcess())

    # Get current limit info
    limits = win32api.QueryInformationJobObject(
        None, win32api.JobObjectExtendedLimitInformation
    )

    # modify limits
    limit_flags = (
        0
        | (win32api.JOB_OBJECT_LIMIT_ACTIVE_PROCESS if max_processes else 0)
        | (win32api.JOB_OBJECT_LIMIT_PROCESS_MEMORY if max_memory else 0)
    )
    limits["BasicLimitInformation"]["LimitFlags"] = limit_flags
    limits["BasicLimitInformation"]["ActiveProcessLimit"] = (
        max_processes + 1 if max_processes else 0
    )
    limits["ProcessMemoryLimit"] = max_memory if max_memory else 0

    # set the limits
    win32api.SetInformationJobObject(
        __job, win32api.JobObjectExtendedLimitInformation, limits
    )


########################################################################################
# functions for testing below this line


def parent():
    print("parent started", os.getpid())
    arr1 = numpy.arange(1024 * 10)
    win32_limit(max_memory=1024 * 10)
    arr2 = numpy.arange(1024 * 10)
    for i in range(3):
        subprocess.Popen("python win32_limit.py /child")

    input("press any key to do stuff to children")

    job_processes = win32api.QueryInformationJobObject(
        None, win32api.JobObjectBasicProcessIdList
    )
    for pid in job_processes:
        if pid == os.getpid():  # Don't kill ourselves
            continue
        print("Killed", pid)


def child():
    print("child running", os.getpid())
    time.sleep(300)


if __name__ == "__main__":
    if "/child" in sys.argv:
        child()
    else:
        parent()
