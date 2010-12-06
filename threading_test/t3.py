from threading import Thread
import os
from Queue import Queue
import time
import sys
from multiprocessing import Process as MPProcess

def contatore():
    cont = 0
    while cont<98765:
        cont += 1
        #time.sleep(0.5)
    print "\n%d \n" % cont

def worker():
    contatore()
        
def contatore_worker_MP(indx):
    print 'worker', indx, avviato
    cont = 0
    while cont<98765:
        cont += 1
    print "\nid: %d, cont = %d \n" % indx, cont

def avvia_contatore(n_contatori):
    for i in range(n_contatori):
        t = Thread(target=worker)
        t.setDaemon(True)
        t.start()
        
def avvia_contatoreMP(n_contatori):
    ps = []
    for i in range(n_contatori):
        p = MPProcess(target=contatore_worker_MP, args=(i,))
        p.start()
        ps.append(p)
    print 'workers avviati!'
    for p in ps:
        p.join()
        

if __name__ == '__main__':
    n_contatori = 1
    #n_workers = 2
    #avvia_contatore(n_contatori)

    avvia_contatoreMP(n_contatori)
    
