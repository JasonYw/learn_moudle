import subprocess#此模块允许我们启动一个新的进程，并连接到他们的输入/输出/错误的管道，从而获取返回值




def base_run():
    #运行外部命令
    #命令行参数以字符串列表传递
    #执行 ls -l /Users/rico/Desktop/learn_moudle
    completed =subprocess.run(['ls','-l','/Users/rico/Desktop/learn_moudle'],timeout=5,check=True,stdout=subprocess.PIPE)
    '''
    stdin、stdout、stdeer:
        子进程的标准输入输出还有错误
        值可以是subprocess.PIPE、subprocess.DEVNULL、文件描述符、一个文件对象或者None
        stderr可以与stdout合并一起输出
    timeout: 超市时间，若超过命令执行时间，子进程被杀死，并弹出timeoutexpireed异常
    check: 若为true->当进程退出状态码不是0，则报错，calledprocesserror
    encoding:指定该参数，stdin，stdout，stderr可以接受字符串数据并以指定编码方式编码，否则只接受bytes类型数据
    shell: 若为true，将通过操作系统的shell执行的指定命令 
    '''
    #completed.returncode -> 查询结果
    print("状态码:",completed.returncode)
    print("捕获到的输出:",completed.stdout) #->为bytes类型，因为没加入enccoding参数
    print('have {} bytes in stdout:\n{}'.format(len(completed.stdout),completed.stdout.decode('utf-8')))
    print("=====================================")
    try:
        completed =subprocess.run(
            'echo to stdout;echo to stderr 1>&2; exit 1',
            check=True,
            shell=True,
            stdout=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        print("eror:",e)
    else:
        print('returncode:',completed.returncode)
        print('have {} bytes in stdout:\n{}'.format(len(completed.stdout),completed.stdout.decode('utf-8')))
    print("=====================================")
    try:
        completed =subprocess.run(
            'echo to stdout;echo to stderr 1>&2; exit 1',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )#当没有check=true时，则不会抛出异常
    except subprocess.CalledProcessError as e:
        print("eror:",e)
    else:
        print('returncode:',completed.returncode)
        print('have {} bytes in stdout:\n{}'.format(len(completed.stdout),completed.stdout.decode('utf-8')))
        print('have {} bytes in stdout:\n{}'.format(len(completed.stderr),completed.stderr.decode('utf-8')))
    print("=====================================")
    try:
        output =subprocess.check_output(
            'echo to stdout;echo to stderr 1>&2;',
            shell=True,
            stderr=subprocess.STDOUT #输出与错误合并
        )
    except subprocess.CalledProcessError as err:
        print("error:",err)
    else:
        print('have {} bytes in output:\n{}'.format(len(output),output.decode('utf-8')))
    print("=====================================")
    try:
        completed =subprocess.run(
            'echo to stdout;echo to stderr 1>&2;exit 1',
            shell=True,
            stdout =subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as err:
        print("error:",err)
    else:
        print('returncode',completed.returncode)
        print('stdout is',completed.stdout)
        print('stderr is',completed.stderr)
    print("=====================================")
    


def base_Popen():
    p =subprocess.Popen("ls -l",shell=True)
    '''
        用于子进程的创建和管理
        第一个参数为shell命令，str、list或者tupe
        bufsize：设置缓冲区大小 0不使用缓冲区，1表示行缓冲。文本模式，正数表示缓冲大小，负数表示使用系统默认的缓冲
        stdin、stout、stderr：表示输入、输出、错误
        sheel为true表示通过shell执行指定命令
        cwd：设置子进程的当前目录
        env：指定子进程的环境变量，env=None，子进程的环境变量从父进程中继承

        p->Popen对象
            poll() 检查进程是否终止，如果终止了返回returncode，佛则返回none
            wait(timeout) 等到子进程终止
            communicate(input,timeout) 和子进程交互，发送和读取数据
            send_signal(singnal) 发送信号到子进程
            terminate()  停止子进程，发送sigterm信号到子进程
            kill() 杀死子进程，发送sigkill信号到子进程 
    '''
    print(p.returncode) 
    print("=====================================")
    p =subprocess.Popen(
        ['echo','"to stdout"'],
        stdout=subprocess.PIPE
    )
    stdout_value =p.communicate()[0].decode('utf-8')
    print('stdout:',repr(stdout_value)) #repr将象转化为供解释器读取的形式
    print("=====================================")
    p =subprocess.Popen(
        ['cat','-'], 
        stdin =subprocess.PIPE
    )
    p.communicate('stdin: to stdin\n'.encode('utf-8'))
    

if __name__ == "__main__":
    #base_run()
    base_Popen()
