from threading import Thread
import os
import subprocess
from Queue import Queue
import logging
import time
import sys
from pbp.scripts.profiler import profile, print_stats

dirname = os.path.realpath(os.path.dirname(__file__))
CONVERTER = os.path.join(dirname, 'converter.py')

q = Queue()
def index_file(filename):
f = open(filename)
try:
content = f.read()
# process is here
subprocess.call([CONVERTER])
finally:
f.close()
def worker():
while True:
index_file(q.get())
q.task_done()
def index_files(files, num_workers):
for i in range(num_workers):
t = Thread(target=worker)
t.setDaemon(True)
t.start()
for file in files:
q.put(file)
q.join()
def get_text_files(dirname):
for root, dirs, files in os.walk(dirname):
for file in files:
if os.path.splitext(file)[-1] != '.txt':
continue
yield os.path.join(root, file)
@profile('process')
def process(dirname, numthreads):
dirname = os.path.realpath(dirname)
if numthreads > 1:
index_files(get_text_files(dirname), numthreads)
else:
for f in get_text_files(dirname):
index_file(f)
if __name__ == '__main__':
process(sys.argv[1], int(sys.argv[2]))
print_stats()
