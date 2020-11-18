import multiprocessing
import time
def multiprocessing_queue():
    class MyFancyClass:
        def __init__(self,name):
            self.name =name
        
        def do_something(self):
            proc_name =multiprocessing.current_process().name
            print(f'Doing something fancy in {proc_name} for {self.name}')
    
    def worker(q):
        obj =q.get()
        obj.do_something()
    
    queue =multiprocessing.Queue()
    p =multiprocessing.Process(target=worker,args=(queue,))
    p.start()
    queue.put(MyFancyClass('Fancy Dan'))
    queue.close()
    queue.join_thread()
    p.join()

def multiprocessing_producer_consumer():
    class Consumer(multiprocessing.Process):
        def __init__(self,task_queue,result_queue):
            multiprocessing.Process.__init__(self)
            self.task_queue =task_queue
            self.result_queue =result_queue

        def run(self):
            proc_name =self.name
            while True:
                next_task =self.task_queue.get()
                if next_task is None:
                    print(f'{proc_name}: exiting')
                    self.task_queue.task_done()
                    break
                print(f"{proc_name} : {next_task}")
                answer =next_task()
                self.task_queue.task_done()
                self.result_queue.put(answer)
        
    class Task:
        def __init__(self,a,b):
            self.a =a
            self.b =b
        
        def __call__(self):
            time.sleep(0.1)
            return f"{self.a} * {self.b} ={self.a*self.b}"

        def __str__(self):
            return f"{self.a} * {self.b}"
    
    tasks =multiprocessing.JoinableQueue()
    results =multiprocessing.Queue()
    num_consumers =multiprocessing.cpu_count() *2
    print(f"creating {num_consumers} consumers")
    consumer =[
        Consumer(tasks,results)
        for i in range(num_consumers)
    ]
    for w in consumer:
        w.start()

    num_jobs =10
    for i in range(num_jobs):
        tasks.put(Task(i,i))
    
    for i in range(num_consumers):
        tasks.put(None)
    
    tasks.join()

    while num_jobs:
        result =results.get()
        print("Result:",result)
        num_jobs -= 1



if __name__ =="__main__":
    multiprocessing_producer_consumer()
    