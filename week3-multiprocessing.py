import multiprocessing


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
        p =multiprocessing.Process(target=worker,args=(1,))
        jobs.append(p)
        p.start()
        

   
if __name__ =="__main__":
    multiprocessing_simpleags()