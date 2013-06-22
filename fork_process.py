"""
The script is create process with NUM_CHILDS forks.
"""

import threading

NUM_CHILDS = 11


class ChildProcess(threading.Thread):
    """
    Child process without functionality. It is just in loop.
    """
    def run(self):
        while True:
            pass

def main():
    for i in xrange(NUM_CHILDS):
        child_process = ChildProcess()
        child_process.start()

if __name__ == "__main__":
    main()
