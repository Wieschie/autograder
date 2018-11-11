from resource import setrlimit, RLIMIT_AS, RLIMIT_NPROC


def posix_limit(max_memory: int = None, max_processes: int = None):
    """
    Sets per-process limits on POSIX (Linux) systems

    Args:
        max_memory: Max memory in bytes that process is allowed to allocate
        max_processes: Max processes allowed to spawn (1 means that the process can not
            spawn children or POSIX threads)
    """
    if max_memory:
        setrlimit(RLIMIT_AS, (max_memory, max_memory))
    if max_processes:
        setrlimit(RLIMIT_NPROC, (max_processes, max_processes))
