import multiprocessing
import time

def wait_for_event(e):
    print("wait for event:starting")
    e.wait()
    print("wait_for_event:e.is_set()->",e.is_set())

def wait_for_event_timeout(e,t):
    print('wait_for_event_timeout:starting')
    e.wait(t)
    print("wait_for_event:e.is_set()->",e.is_set())

if __name__ =="__main__":
    #event 从threading那里克隆过来的
    e =multiprocessing.Event()
    w1 =multiprocessing.Process(name='block',target=wait_for_event,args=(e,))
    w1.start()
    
    w2 =multiprocessing.Process(
        name='nonblock',
        target=wait_for_event_timeout,
        #args=(e,4)
        args=(e,2)
    )
    w2.start()

    print('main:waiting before calling Event.set()')
    time.sleep(3)
    e.set()
    print('main:event is set')
