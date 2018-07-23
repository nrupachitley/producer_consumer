from __future__ import print_function
from threading import Thread, Lock, Semaphore, current_thread
import time
import random

lock = Lock()

BUFFER = []
BUFFER_SIZE = 10
full = Semaphore(0)
empty = Semaphore(BUFFER_SIZE)

IN = 0
OUT = 0


def insertItem(item_entered):
    global IN, OUT
    flag = 0
    if (IN + 1) % BUFFER_SIZE != OUT:
        BUFFER[IN] = item_entered
        IN = (IN + 1) % BUFFER_SIZE
    else:
        flag = -1
    return flag


def removeItem():
    global IN, OUT
    flag = 0
    item_removed = 0

    if IN != OUT:
        item_removed = BUFFER[OUT]
        BUFFER[OUT] = -1
        OUT = (OUT + 1) % BUFFER_SIZE
    else:
        flag = -1
    return flag, item_removed


class Producer(Thread):
    def run(self):
        nums = range(20)
        global BUFFER
        while True:
            time.sleep(sleepTime)
            num = random.choice(nums)

            empty.acquire()
            lock.acquire()
            flag = insertItem(num)
            if flag == -1:
                print("{} waiting!".format(self.getName()))
            else:
                print("{} produced by {} at {}".format(num, self.getName(), (BUFFER_SIZE - 1) if IN == 0 else (IN - 1)))
            print("Buffer:", BUFFER)
            lock.release()
            full.release()


class Consumer(Thread):
    def run(self):
        global BUFFER
        while True:
            time.sleep(sleepTime)

            full.acquire()
            lock.acquire()
            flag, item = removeItem()
            if flag == -1:
                print("{} waiting!".format(self.getName()))
            else:
                print("{} consumed by {} at {}".format(item, self.getName(), (BUFFER_SIZE - 1) if OUT == 0 else (OUT - 1)))
            print("Buffer:", BUFFER)

            lock.release()
            empty.release()


if __name__ == '__main__':
    sleepTime = input("Insert sleep time for Producer and Consumer threads in seconds: ")
    numberOfProducers = input("Insert number of Producer threads: ")
    numberOfConsumers = input("Insert number of Consumer threads: ")

    BUFFER = [-1] * BUFFER_SIZE

    threads = []
    for p in range(numberOfProducers):
        myProducer = Producer(name="Producer-{}".format(p+1))
        threads.append(myProducer)

    for c in range(numberOfConsumers):
        myConsumer = Consumer(name="Consumer-{}".format(c+1))
        threads.append(myConsumer)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    time.sleep(sleepTime)

    print("End")

