from threading import Thread
import os
from Queue import Queue
import time
import sys

def stampatore(char):
    for i in range(10):
        print char, i
        #time.sleep(0.5)

q = Queue()
        
def worker():
    while True:
        stampatore(q.get())
        q.task_done()

def avvia_stampatore(start_char, n_char, num_workers):
    for i in range(num_workers):
        t = Thread(target=worker)
        t.setDaemon(True)
        t.start()
    for i in range(n_char):
        q.put(chr(ord(start_char) + i))
    q.join()


if __name__ == '__main__':
    avvia_stampatore('c', 15, 8)
