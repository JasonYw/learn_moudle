import threading
import time
import logging
import random
#当主线程执行完毕后，子线程随即停止
#线程共享的环境包括进程代码段、进程的公有数据等，利用这些共享的数据，线程之间很容易实现通信。
#设置守护线程之后，当主线程结束时，子线程也将立即结束
#join让主线程等待其他线程结束

def model0():

    def work0(t):
        print(threading.current_thread().getName(),'starting')
        time.sleep(int(t))
        print(threading.current_thread().getName(),'exiting')

    def work1(t):
        print(threading.current_thread().getName(),'starting')
        time.sleep(int(t))
        print(threading.current_thread().getName(),'exiting')

    a0 =threading.Thread(name="work0",target=work0,args=(1,))
    a1 =threading.Thread(name='work1',target=work1,args=(1,))  
    a2 =threading.Thread(target=work0,args=(1,)) #使用默认的名字
    a1.start()
    a0.start()
    a2.start()


def model1():

    def work2():
        logging.debug('starting')
        time.sleep(2)
        logging.debug('exting')

    def work3():
        logging.debug('starting')
        time.sleep(0.2)
        logging.debug('exting')
    #%(message)s	日志记录的文本内容，通过 msg % args计算得到的
    #%(levelname)s	该日志记录的文字形式的日志级别（‘DEBUG’, ‘INFO’, ‘WARNING’, ‘ERROR’, ‘CRITICAL’）
    #%(threadName)-10s 拿到线程名字
    logging.basicConfig(
        level=logging.DEBUG,
        format ='[%(levelname)s] (%(threadName)-10s) %(message)s',
    )
    b0 =threading.Thread(name='work2',target=work2)
    b1 =threading.Thread(name='work3',target=work3)
    b2 =threading.Thread(target=work2)
    b0.start()
    b1.start()
    b2.start()

def model2():
    def work3():
        logging.debug('starting')
        time.sleep(0.2)
        logging.debug('exting')

    def non_daemon():
        logging.debug('statring')
        logging.debug('exiting')

    logging.basicConfig(
        level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s',
    )
    c0 =threading.Thread(name='daemon',target=work3,daemon=True) #标记为守护线程
    c1 =threading.Thread(name='non-demon',target=non_daemon)
    c0.start()
    c1.start()
    

    c0.join(0.3) #使用join可以等待守护线程退出,传入一个数字，表示阻塞时间,因为时间小于work3中的时间，所以无法看到work3结束的消息
    print('c1.isAlive():',c1.is_alive())
    print('c0.isAlive():',c0.is_alive())

def model3(): 
    
    def work4():
        pause =random.randint(1,5)/10
        logging.debug('sleeping %0.2f',pause)
        time.sleep(pause)
        logging.debug('ending')

    logging.basicConfig(
        level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s',
    )

    for i in range(3):
        d =threading.Thread(target=work4,daemon=True)
        d.start()
        
    main_thread =threading.main_thread() #是Python中线程模块的内置方法。 它用于返回主线程对象

    for d in threading.enumerate(): #返回存活的thread实例
        if d is main_thread: #不跳过去会导致死锁
            #print('current thread:',d.getName())
            continue
        else:
            logging.debug('joining %s',d.getName())
            d.join()
    


def model4():
    class myThread(threading.Thread):
        def __init__(self,group=None,target=None,name=None,args=(),kwargs=None,*,daemon=True):
            super().__init__(group=group,target=target,name=name,daemon=daemon)
            self.args =args
            self.kwargs =kwargs

        def run(self):
            logging.debug('running %s and %s',self.args,self.kwargs)

    logging.basicConfig(
        level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s'
    )

    for i in range(5):
        e =myThread(args=(i,),kwargs={'a':'A','b':'B'})
        e.start()

def model5():

    def work5():
        print(time.strftime('%H:%M:%S',time.localtime()))
        logging.debug('working running 0')
        # time.sleep(1)
        # logging.debug('working running 1')

    logging.basicConfig(
        level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s'
    )

    f0 =threading.Timer(1,work5) #在延时后，timer开始工作,threading.Timer创建的是一个线程！这个细节要注意，定时器基本上都是在线程中执行
    f0.setName('f0') 
    f1 =threading.Timer(1,work5)
    f1.setName('f1')

    print(time.strftime('%H:%M:%S',time.localtime()))
    logging.debug('starting timers')
    f0.start()
    f1.start()
    print(time.strftime('%H:%M:%S',time.localtime()))
    logging.debug('waiting befor canceling %s',f1.getName())
    time.sleep(2)
    print(time.strftime('%H:%M:%S',time.localtime()))
    logging.debug('canceling %s',f1.getName())
    f0.cancel()
    logging.debug('done')


def model6():
    def wait_for_event(e):
        logging.debug('wait_for_event starting')
        event_is_set =e.wait()
        logging.debug('wait_for_event starting event set: %s',event_is_set)

    def wait_for_event_timeout(e,t):
        #while not e.is_set():
        logging.debug('wait_for_event_timeout starting')
        event_is_set =e.wait(t) #t表示为一个时间，调用该方法的线程会被阻塞,超过时间返回一个布尔值，线程会停止阻塞继续执行 指示是否设置了事件
        logging.debug('wait_for_event_timeout event set: %s',event_is_set)  #event.isSet()：判断event的标志是否为True。
        if event_is_set:
            logging.debug('processing event')
        else:
            logging.debug('doing other work')

    logging.basicConfig(
        level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s'
    )

    event_ =threading.Event()
    #通过threading.Event()可以创建一个事件管理标志，该标志（event）默认为False
    #event.wait(timeout=None)：调用该方法的线程会被阻塞，如果设置了timeout参数，超时后，线程会停止阻塞继续执行；
    #event.clear()：将event的标志设置为False，调用wait方法的所有线程将被阻塞；
   
    g0 =threading.Thread(
        name='block',
        target=wait_for_event,
        args=(event_,)
    )
    g0.start()

    g1 =threading.Thread(
        name ="nonblock",
        target=wait_for_event_timeout,
        args=(event_,0.1),
        #daemon=True
    )
    g1.start()

    logging.debug('waiting before calling event.set()')
    time.sleep(1)
    event_.set()#event.set()：将event的标志设置为True，调用wait方法的所有线程将被唤醒；
    logging.debug('event is set')


def model7():

    class Counter():
        def __init__(self,start=0):
            self.lock =threading.Lock() #lock 防止两个线程同时更改其内部状态
            self.value =start
        
        def increment(self):
            logging.debug('waiting for lock')
            self.lock.acquire() #获取一把锁
            try:
                logging.debug('acquired lock')
                self.value =self.value+1
            finally:
                self.lock.release() #释放锁，不管发生什么，释放锁

    def worker(c):
        for i in range(2):
            pause =random.random()
            logging.debug('sleeping %0.02f',pause)
            time.sleep(pause)
            c.increment()
        logging.debug('Done')
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s'
    )

    counter =Counter()
    for i in range(2):
        h =threading.Thread(target=worker,args=(counter,))
        h.start()
    
    logging.debug('waiting for worker threads')
    main_thread =threading.main_thread()
    for i in threading.enumerate():
        if i is not main_thread:
            i.join()
    logging.debug('Counter: %d',counter.value)

def model8():
    def lock_holder(lock):
        logging.debug('Starting')
        while True:
            lock.acquire()
            try:
                logging.debug('Holding')
                time.sleep(0.5)
            finally:
                logging.debug('Not holding')
                lock.release()
            time.sleep(0.5)

    def worker(lock):
        logging.debug('Starting')
        num_tries =0
        num_acquires =0
        while num_acquires <3:
            time.sleep(0.5)
            logging.debug('Trying to acquire')
            have_it =lock.acquire(0)
            try:
                num_tries += 1
                if have_it:
                    logging.debug("Iteration %d: Acquired",num_tries)
                else:
                    logging.debug("Iteration %d: Not Acquired",num_tries)    
            finally:
                if have_it:
                    lock.release()
        logging.debug('done after %d iterations',num_tries)

    logging.basicConfig(
        level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s'
    )

    lock =threading.Lock()

    holder =threading.Thread(
        target=lock_holder,
        args=(lock,),
        name='LockHolder',
        daemon=True
    )

    holder.start()

    worker_t =threading.Thread(
        target=worker,
        args=(lock,),
        name='Worker'
    )

    worker_t.start()


def model9():
    lock =threading.RLock()
    print('First try:',lock.acquire())
    print('second try:',lock.acquire(0))


def model10():
    def worker_with(lock):
        with lock:
            logging.debug('lock acquired via with')

    def worker_no_with(lock):
        lock.acquire()
        try:
            logging.debug('lock acquired directly')
        finally:
            lock.release()

    logging.basicConfig(
        level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s'
    )

    lock =threading.Lock()
    j0 =threading.Thread(target=worker_with,args=(lock,))
    j1 =threading.Thread(target=worker_no_with,args=(lock,)) 

    j0.start()
    j1.start()

def model11():
    def consumer(cond):
        logging.debug('starting consumer thread')
        with cond:
            cond.wait() #设置等待
            logging.debug('resource is available to consumer')
    
    def producer(cond):
        logging.debug('starting producer thread')
        with cond:
            logging.debug('making resource available')
            cond.notifyAll() #设置条件，通知线程
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s'
    )

    condition =threading.Condition()
    h0 =threading.Thread(name='c1',target=consumer,args=(condition,))
    h1 =threading.Thread(name='c2',target=consumer,args=(condition,))
    h2 =threading.Thread(name='p',target=producer,args=(condition,))

    h0.start()
    time.sleep(0.2)
    h1.start()
    time.sleep(0.2)
    h2.start()

def model12():
    def worker(barrier):
        print(threading.current_thread().name,'waiting for barrier with {} others'.format(barrier.n_waiting))
        worker_id =barrier.wait()
        print(threading.current_thread().name,'after barrier',worker_id)
    
    NUM_THREADS =3
    barrier =threading.Barrier(NUM_THREADS)
    threads =[
        threading.Thread(
            name='worker-%s' % i,
            target=worker,
            args=(barrier,),
        )
        for i in range(NUM_THREADS)
    ]

    for t in threads:
        print(t.name,'starting')
        t.start()
        time.sleep(0.1)
    
    for t in threads:
        t.join()


def model13():
    def worker(barrier):
        print(threading.current_thread().name,'waiting for barrier with {} others'.format(barrier.n_waiting))
        try:
            worker_id =barrier.wait()
        except threading.BrokenBarrierError:
            print(threading.current_thread().name,'aborting')
        else:
            print(threading.current_thread().name,'after barrier',worker_id)
    
    NUM_THREADS =3
    barrier =threading.Barrier(NUM_THREADS+1)


    threads =[
        threading.Thread(
            name='worker-%s' % i,
            target=worker,
            args=(barrier,),
        )
        for i in range(NUM_THREADS)
    ]

    for t in threads:
        print(t.name,'starting')
        t.start()
        time.sleep(0.1)
    
    barrier.abort() #引发异常

    for t in threads:
        t.join()

def model14():
    class ActivePool():
        def __init__(self):
            super(ActivePool,self).__init__()
            self.active =[]
            self.lock =threading.Lock()
        
        def makeActive(self,name):
            with self.lock:
                self.active.append(name)
                logging.debug('Running:%s',self.active)
        
        def makeInactive(self,name):
            with self.lock:
                self.active.remove(name)
                logging.debug('Running:%s',self.active)

    def worker(s,pool):
        logging.debug('waiting to join the pool')
        with s:
            name =threading.current_thread().getName()
            pool.makeActive(name)
            time.sleep(0.1)
            pool.makeInactive(name)
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s'
    )

    pool =ActivePool()
    s =threading.Semaphore(2)
    for i in range(4):
        t =threading.Thread(
            target=worker,
            name=str(i),
            args=(s,pool)
        )
        t.start()

def model15():
    def show_value(data):
        try:
            val =data.value
        except AttributeError:
            logging.debug('No value yet')
        else:
            logging.debug('value=%s',val)
    
    def worker(data):
        show_value(data)
        data.value =random.randint(1,100)
        show_value(data)
    
    class mylocal(threading.local):
        def __init__(self,value):
            super().__init__()
            logging.debug('Initializing %r',self)
            self.value =value

    logging.basicConfig(
        level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s'
    )

    # local_data =threading.local()
    # show_value(local_data)
    # local_data.value =1000
    # show_value(local_data)
    local_data =mylocal(1000)
    show_value(local_data)

    for i in range(2):
        t =threading.Thread(target=worker,args=(local_data,))
        t.start()


if __name__ == "__main__":
    model6()
