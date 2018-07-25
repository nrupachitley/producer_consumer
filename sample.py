from __future__ import print_function
from threading import Thread, Lock, Semaphore, Event, current_thread
import os, time, random

lock = Lock()
BUFFER = []
BUFFER_SIZE = 10
full = Semaphore(0)
empty = Semaphore(BUFFER_SIZE)

IN = 0
OUT = 0
stop_it = Event()


def insertItem(item_entered):
    global IN, OUT
    flag = 0
    empty.acquire(False)
    lock.acquire()
    if (IN + 1) % BUFFER_SIZE != OUT:
        BUFFER[IN] = item_entered
        IN = (IN + 1) % BUFFER_SIZE
        print("{} produced by {} at {}".format(item_entered, current_thread().getName(), (BUFFER_SIZE - 1) if IN == 0 else (IN - 1)))
        print("Buffer:", BUFFER)
        print()
    else:
        flag = -1
    if flag == -1:
        print("{} waiting!".format(current_thread().getName()))
    lock.release()
    full.release()
    return flag


def removeItem():
    global IN, OUT
    flag = 0
    item_removed = 0
    full.acquire(False)
    lock.acquire()
    if IN != OUT:
        item_removed = BUFFER[OUT]
        BUFFER[OUT] = -1
        OUT = (OUT + 1) % BUFFER_SIZE
        print("{} consumed by {} from {}".format(item_removed, current_thread().getName(), (BUFFER_SIZE - 1) if OUT == 0 else (OUT - 1)))
        print("Buffer:", BUFFER)
        print()
    else:
        flag = -1
    if flag == -1:
        print("{} waiting!".format(current_thread().getName()))
    lock.release()
    empty.release()
    return flag, item_removed


class Producer(Thread):
    def run(self):
        nums = range(20)
        global BUFFER
        while True:
            time.sleep(sleepTimeProducer)
            num = random.choice(nums)
            insertItem(num)
            if stop_it.is_set():
                break


class Consumer(Thread):
    def run(self):
        global BUFFER
        while True:
            time.sleep(sleepTimeConsumer)
            removeItem()
            if stop_it.is_set():
                break


if __name__ == '__main__':
    sleepTimeProducer = input("Insert sleep time for Producer in seconds: ")
    sleepTimeConsumer = input("Insert sleep time for Consumer in seconds: ")
    numberOfProducers = input("Insert number of Producer threads: ")
    numberOfConsumers = input("Insert number of Consumer threads: ")
    print()
    BUFFER = [-1] * BUFFER_SIZE
    threads = []
    start_time = time.time()
    for p in range(numberOfProducers):
        myProducer = Producer(name="Producer-{}".format(p+1))
        threads.append(myProducer)
    for c in range(numberOfConsumers):
        myConsumer = Consumer(name="Consumer-{}".format(c+1))
        threads.append(myConsumer)
    for t in threads:
        t.start()
    while time.time() - start_time < 10:
        pass

    stop_it.set()
    for t in threads:
        print("This thread is ending!!!!!!", t.getName())
        t.join(timeout=1)
    os._exit(0)

