from win32api import GetCurrentProcess, OpenProcess
from win32job import *

import os
import subprocess
import time
import sys


def win32_limit(job):
    # Get current limit info
    limits = QueryInformationJobObject(None, JobObjectExtendedLimitInformation)
    # modify limits
    limit_flags = JOB_OBJECT_LIMIT_ACTIVE_PROCESS | JOB_OBJECT_LIMIT_PROCESS_MEMORY
    limits["BasicLimitInformation"]["LimitFlags"] = limit_flags
    limits["BasicLimitInformation"]["ActiveProcessLimit"] = 5
    limits["ProcessMemoryLimit"] = 10 ** 20 * 32
    # set the limits
    SetInformationJobObject(job, JobObjectExtendedLimitInformation, limits)


def parent():
    print("parent started", os.getpid())
    job = CreateJobObject(None, "autograder-job")
    AssignProcessToJobObject(job, GetCurrentProcess())
    win32_limit(job)

    for i in range(3):
        subprocess.Popen("python main.py /child")

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
