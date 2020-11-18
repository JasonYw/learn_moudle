import multiprocessing
import time


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
                print(f'{proc_name}:exiting')
                #指出之前进入队列的任务已经完成 由消费者进程使用，对于每次取出get获取的任务执行完成后调用task_done 告诉队列改任务已经完成
                #若此方法被调用的次数多与放入队列的次数，将会引发valueerror异常
                self.task_queue.task_done() 
                break
            print(f"{proc_name}:{next_task}")
            answer =next_task() #执行Task__call__方法
            self.task_queue.task_done()
            self.result_queue.put(answer)
    
class Task:
    def __init__(self,a,b):
        self.a=a
        self.b=b
    
    def __call__(self):
        time.sleep(1)
        return f"{self.a} * {self.b} = {self.a*self.b}"

    def __str__(self):
        return f'{self.a} * {self.b}'
        #return '{self.a} * {self.b}'.format(self=self)
    
if __name__ =="__main__":
    #JoinableQueue 是Queue的子类，额外添加了task_done和join方法
    tasks =multiprocessing.JoinableQueue()
    results =multiprocessing.Queue()
    #创建cpu进程数量的两倍的进程数
    num_consumers =multiprocessing.cpu_count()*2
    print(f'creating {num_consumers} consumers')
    consumers =[
        Consumer(tasks,results)
        for i in range(num_consumers)
    ]
    for w in consumers:
        w.start()
    
    num_jobs =10
    for i in range(num_jobs):
        tasks.put(Task(i,i))
    
    for i in range(num_consumers):
        tasks.put(None)
    
    tasks.join()

    while num_jobs:
        print('Results:',results.get())
        num_jobs -=1

