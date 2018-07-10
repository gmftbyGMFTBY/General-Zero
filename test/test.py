#!/usr/bin/python3
# Author: GMFTBY
# Time  : 2018.7.9

'''
test the multiproceses
'''

import multiprocessing as mp
import os
import time

def run(name):
    print("This is the processing %s (%s)" % (name , os.getpid()))
    if name != 4 : time.sleep(5)

print("Parent processing %s" % os.getpid())   # print the PID of the parent processing.
for i in range(5):
    p = mp.Process(target = run , args = (i,))    # 这里必须要写成(i,)的形式，因为要求args是可迭代的，一个值是不可以迭代的
    print("processing will start.")
    p.start()
    p.join()     #　父进程只有在当前的这个循环的子进程p结束之后才会进入下一个循环
print('End!')
