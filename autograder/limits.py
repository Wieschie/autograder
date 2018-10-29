from resource import setrlimit, RLIMIT_AS, RLIMIT_NPROC


def limit(max_memory: int = None, max_processes: int = None):
    if max_memory:
        setrlimit(RLIMIT_AS, (max_memory, max_memory))
    if max_processes:
        setrlimit(RLIMIT_NPROC, (max_processes, max_processes))
