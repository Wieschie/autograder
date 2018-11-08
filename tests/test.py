import sys


def parent():
    from resource import setrlimit, RLIMIT_AS, RLIMIT_NPROC
    import subprocess

    print("Setting memory limit")
    setrlimit(RLIMIT_AS, (5_820_500, sys.maxsize))
    proc = subprocess.run(["./alloc", "100"])
    print(proc)
    print(f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}")


def child():
    import numpy as np

    print("Child called")
    s = 0
    arr = []
    for x in range(100):
        arr.append(np.arange(1000))
        s += len(arr[x])
        print(f"Allocated {s}")


if __name__ == "__main__":
    if "/child" in sys.argv:
        child()
    else:
        parent()
