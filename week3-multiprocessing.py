import multiprocessing
import week3_multiprocessing_import
import time
import sys
import logging


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
        print('starting:',p.name,p.pid)
        sys.stdout.flush()
        #在Linux系统下，必须加入sys.stdout.flush()才能一秒输一个数字
        #在Windows系统下，加不加sys.stdout.flush()都能一秒输出一个数字
        time.sleep(2)
        print('exiting:',p.name,p.pid)
        sys.stdout.flush()
    
    def non_daemon():
        p=multiprocessing.current_process()
        print('starting:',p.name,p.pid)
        sys.stdout.flush()
        time.sleep(2)
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

def multiprocessing_daemon_join():
    def daemon():
        name =multiprocessing.current_process().name
        print('starting:',name)
        time.sleep(2)
        print('exiting:',name)
    
    def non_daemon():
        name =multiprocessing.current_process().name
        print('starting:',name)
        print('exiting:',name)

    d =multiprocessing.Process(
        name ='daemon',
        target=daemon
    )  
    d.daemon =True

    n =multiprocessing.Process(
        name ='non-daemon',
        target=non_daemon
    )
    n.daemon =False

    d.start()   
    n.start()

    d.join(3)
    print('d.is_alive()',d.is_alive())
    n.join()    

def multiprocessing_terminate():
    def slow_worker():
        print('starting workrt')
        time.sleep(0.2)
        print('finished worker')

    p =multiprocessing.Process(target=slow_worker)
    print('BEFORE',p,p.is_alive())

    p.start()
    print('DURING:',p,p.is_alive())

    time.sleep(0.1)
    p.terminate()
    print('TERMINATED',p,p.is_alive())

    p.join()
    print('JOINED:',p,p.is_alive())

def multiprocessing_exitcode():
    def exit_error():
        sys.exit(1)
    
    def exit_ok():
        return
    
    def return_value():
        return 1
    
    def rais_runtimeError():
        raise RuntimeError('There was an error!')
    
    def terminated():
        time.sleep(3)

    jobs =[]
    funcs =[
        exit_error,
        exit_ok,
        return_value,
        rais_runtimeError,
        terminated,
    ]    
    for fuc in funcs:
        print('starting process for',fuc.__name__)
        j =multiprocessing.Process(target=fuc,name =fuc.__name__)
        jobs.append(j)
        j.start()
    
    jobs[-1].terminate()
    
    for job in jobs:
        #exitcode ==0:没有产生错误 >0 该过程有一个错误，并推出该代码   <0 这个过程杀死了-1*exitcode
        job.join()
        print('{:>15}.exitcode ={}'.format(job.name,job.exitcode))
    

def multiprocessing_log_to_stderr():
    def worker():
        print('Doing some work')
        sys.stdout.flush()

    multiprocessing.log_to_stderr(logging.DEBUG)
    logger =multiprocessing.get_logger()     #通过get_logger来设置记录
    logger.setLevel(logging.INFO)
    p =multiprocessing.Process(target=worker)
    p.start()
    p.join()


def multiprocessing_subclass():
    #重写run方法
    class Worker(multiprocessing.Process):
        def run(self):
            print('In{}'.format(self.name))
            return

    jobs =[]
    for i in range(5):
        p =Worker()
        jobs.append(p)
        p.start()
    
    for j in jobs:
        j.join()


if __name__ =="__main__":
    multiprocessing_subclass()
