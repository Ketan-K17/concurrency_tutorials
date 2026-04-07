# JUST A TEST PYTHON SCRIPT TO RUN THE CODE WRITTEN IN THE JUPYTER NOTEBOOKS 

import threading
from multiprocessing import Process
import time
import os

def MyTask():
    print("Starting")
    time.sleep(2)

if __name__ == '__main__':
    t0 = time.time()
    threads = []
    for i in range(10):
        thread = threading.Thread(target=MyTask)
        thread.start()
        threads.append(thread)

    t1 = time.time()
    print("Total Time for Creating 10 Threads: {} seconds".format(t1-t0))

    for thread in threads:
        thread.join()

    t2 = time.time()
    procs = []
    for i in range(10):
        process = Process(target=MyTask)
        process.start()
        procs.append(process)

    t3 = time.time()
    print("Total Time for Creating 10 Processes: {} seconds".format(t3-t2))
    for proc in procs:
        proc.join()

# NOTE: on MacOs / Windows, new processes are created by default using the 'spawn' mode. On linux, the default is 'fork'. What this means is that you should always guard process creation with an if __name__ == '__main__' block. It's fine if you've written process creation code in a function, so long as that code is called in the main block..

# threads is fine everywhere...

# the guard is because you need to have processes created ONLY in the main process, not child processes.