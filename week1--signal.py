'''
信号编号	名称	默认动作	说明
1	SIGHUP	终止	终止控制终端或进程
2	SIGINT	终止	由键盘引起的终端(Ctrl-c)
3	SIGQUIT	dump	控制终端发送给进程的信号, 键盘产生的退出(Ctrl-\),
4	GIGILL	dusmp	非法指令引起
5	SIGTRAP	dump	debug中断
6	SIGABRT/SIGIOT	dump	异常中止
7	SIGBUS/SIGEMT	dump	总线异常/EMT指令
8	SIGFPE	dump	浮点运算溢出
9	SIGKILL	终止	强制杀死进程(大招, 进程不可捕获)
10	SIGUSR1	终止	用户信号, 进程可自定义用途
11	SIGSEGV	dump	非法内存地址引起
12	SIGUSR2	终止	用户信号, 进程可自定义用途
13	SIGPIPE	终止	向某个没有读取的管道中写入数据
14	SIGALRM	终止	时钟中断(闹钟)
15	SIGTERM	终止	进程终止(进程可捕获)
16	SIGSTKFLT	终止	协处理器栈错误
17	SIGCHLD	忽略	子进程退出或中断
18	SIGCONT	继续	如进程停止状态则开始运行
19	SIGSTOP	停止	停止进程运行
20	SIGSTP	停止	键盘产生的停止
21	SIGTTIN	停止	后台进程请求输入
22	SIGTTOU	停止	后台进程请求输出
23	SIGURG	忽略	socket发送紧急情况
24	SIGXCPU	dump	CPU时间限制被打破
25	SIGXFSZ	dump	文件大小限制被打破
26	SIGVTALRM	终止	虚拟定时时钟
27	SIGPROF	终止	profile timer clock
28	SIGWINCH	忽略	窗口尺寸调整
29	SIGIO/SIGPOLL	终止	I/O可用
30	SIGPWR	终止	电源异常
31	SIGSYS/SYSUNUSED	dump	系统调用异常
'''

import signal
import sys
import time
import os
import threading

def example1():
    def recive(signum,stack):
        print('received',signum,'stack:',stack)

    signal.signal(signal.SIGUSR1,recive)
    signal.signal(signal.SIGUSR2,recive)

    print('my pid:',os.getpid())

    while True:
        print("waiting")
        time.sleep(3)
  
def example2():

    def alarm_received(n, stack):
        return


    signal.signal(signal.SIGALRM, alarm_received)

    signals_to_names = {
        getattr(signal, n): n
        for n in dir(signal)
        if n.startswith('SIG') and '_' not in n
    }

    for s, name in sorted(signals_to_names.items()):
        handler = signal.getsignal(s) #获取信号有没有绑定信号事件
        if handler is signal.SIG_DFL: #判断有没有绑定事件，没有的话进行设置
            handler = 'SIG_DFL'
        elif handler is signal.SIG_IGN:
            handler = 'SIG_IGN'
        print('{:<10} ({:2d}):'.format(name, s), handler)

def example3():
    def receive_alarm(signum,stack):
        print("alarm:",time.time())

    signal.signal(signal.SIGALRM,receive_alarm)
    signal.alarm(2) #当程序停留超过两秒则自动，发出信号

    print("1:",time.ctime())
    time.sleep(4)
    print("2:",time.ctime())

def example4():
    def to_exit(sig,stack):
        raise SystemExit("exting")

    signal.signal(signal.SIGINT,signal.SIG_IGN)
    signal.signal(signal.SIGUSR1,to_exit)

    print("my pid:",os.getpid())

    signal.pause()

def example5():
    def signal_handler(num,stack):
        print('recived signal {} in {}'.format(num,threading.currentThread
        ().name))

        signal.signal(signal.SIGUSR1
        ,signal_handler)

    def wait_for_siganl():
        print('waiting for signal in',threading.currentThread().name)
        signal.pause()
        print("done wait")

    receiver =threading.Thread(
        target=wait_for_siganl,
        name='receiver'
    )
    
    receiver.start()
    time.sleep(0.1)

    def send_signal():
        print("sending signal in",threading.currentThread().name)
        os.kill(os.getpid(),signal.SIGUSR1
        )
    
    sender =threading.Thread(target=send_signal,name="sender")
    sender.start()
    sender.join()

    print('waiting for',receiver.name)
    signal.alarm(2)
    receiver.join()

def example6():
    def signal_handler(num,stack):
        print(time.ctime(),'alarm in',threading.currentThread().name)
    
    signal.signal(signal.SIGALRM,signal_handler)

    def usr_alarm():
        t_name =threading.currentThread().name
        print(time.ctime(),'Setting alarm in',t_name)
        signal.alarm(1)
        print(time.ctime(),'sleeping in',t_name)
        time.sleep(3)
        print(time.ctime(),'done with sleep in',t_name)

    alarm_thread =threading.Thread(
        target=usr_alarm,
        name='alarm_thread'
    )

    alarm_thread.start()
    time.sleep(0.1)

    print(time.ctime(),'waiting for',alarm_thread.name)
    alarm_thread.join()

    print(time.ctime(),'exiting normally')

if __name__ =="__main__":
    example2()

