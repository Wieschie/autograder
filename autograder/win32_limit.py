from win32api import GetCurrentProcess, OpenProcess
from win32job import *

import os
import subprocess
import time
import sys


def win32_limit():
    job = CreateJobObject(None, "autograder-job")
    AssignProcessToJobObject(job, GetCurrentProcess())

    # Get current limit info
    limits = QueryInformationJobObject(None, JobObjectBasicLimitInformation)

    # modify limits
    limit_flags = JOB_OBJECT_LIMIT_ACTIVE_PROCESS | JOB_OBJECT_LIMIT_WORKINGSET
    limits["LimitFlags"] = limit_flags
    limits["ActiveProcessLimit"] = 5
    limits["MinimumWorkingSetSize"] = 10
    limits["MaximumWorkingSetSize"] = 10 ** 20 * 32

    # set the limits
    SetInformationJobObject(job, JobObjectBasicLimitInformation, limits)


def parent():
    print("parent started", os.getpid())

    win32_limit()

    for i in range(3):
        subprocess.Popen("python win32_limit.py /child")

    input("press any key to do stuff to children")

    job_processes = QueryInformationJobObject(None, JobObjectBasicProcessIdList)
    for pid in job_processes:
        if pid == os.getpid():  # Don't kill ourselves
            continue
        print("Killed", pid)


def child():
    print("child running", os.getpid())
    time.sleep(300)


if __name__ == '__main__':
    if "/child" in sys.argv:
        child()
    else:
        parent()
