import multiprocessing
import week3_multiprocessing_import
import time
import sys

def multiprocessing_simple():
    def worker():
        print('worker')
    for i in range(5):
        jobs =[]
        p=multiprocessing.Process(target=worker)
        jobs.append(p)
        p.start()

def multiprocessing_simpleags():
    def worker(num):
        print("worker",num)
    jobs =[]
    for i in range(5):
        p =multiprocessing.Process(target=worker,args=(i,))
        jobs.append(p)
        p.start()

def multiprocessing_import_main():
    jobs =[]
    for i in range(5):
        p =multiprocessing.Process(
            target=week3_multiprocessing_import.worker,
        )
        jobs.append(p)
        p.start()

def multiprocessing_names():
    def  worker():
        name=multiprocessing.current_process().name #获取当前进程的名字
        print(name,'Starting')
        time.sleep(2)
        print(name,'Exiting')
    
    def my_service():
        name =multiprocessing.current_process().name
        print(name,'Staring')
        time.sleep(3)
        print(name,'Exiting')
    
    service =multiprocessing.Process(
        name="my_service",
        target=my_service,
    )

    worker_1 =multiprocessing.Process(
        name="worker_1",
        target=worker,
    )

    worker_2 =multiprocessing.Process(
        target=worker,
    )

    worker_1.start()
    worker_2.start()
    service.start()

def multiprocessing_daemon():
    def daemon():
        p=multiprocessing.current_process()
        print('starting:',p.name,p.id)
        sys.stdout.flush()
        time.sleep(2)
        print('exiting:',p.name,p.pid)
        sys.stdout.flush()
    
    def non_daemon():
        p=multiprocessing.current_process()
        print('starting:',p.name,p.pid)
        sys.stdout.flush()
        print('exiting:',p.name,p.pid)
        sys.stdout.flush()

    d =multiprocessing.Process(
        name='daemon',
        target=daemon,
    )
    d.daemon =True

    n =multiprocessing.Process(
        name='non-daemon',
        target=non_daemon,
    )
    
    n.daemon =False

    d.start()
    time.sleep(1)
    n.start()


    
   
if __name__ =="__main__":
    multiprocessing_daemon()