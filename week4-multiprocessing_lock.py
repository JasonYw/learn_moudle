import multiprocessing
import sys

def worker_with(lock,stream):
    with lock:
        stream.write('LOCK ACQUIRED VIA WITH')

def worker_no_with(lock,stream):
    lock.acquire()
    try:
        stream.write('lock acquired directly')
    finally:
        lock.release()

if __name__ =="__main__":
    lock =multiprocessing.Lock()
    w =multiprocessing.Process(
        target=worker_with,
        args=(lock,sys.stdout)
    )

    nw =multiprocessing.Process(
        target=worker_no_with,
        args=(lock,sys.stdout)
    )

    w.start()
    nw.start()
   
    w.join()
    nw.join()
   