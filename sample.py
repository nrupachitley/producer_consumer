from __future__ import print_function
from threading import Thread, Lock, Semaphore
import time
import random

lock = Lock()

BUFFER = []
BUFFER_SIZE = 5
full = Semaphore(0)
empty = Semaphore(BUFFER_SIZE)

IN = 0
OUT = 0
# count = 0

def insertItem(item_entered):
    global IN, OUT
    if (IN + 1) % BUFFER_SIZE != OUT:
        BUFFER[IN] = item_entered
        IN = (IN + 1) % BUFFER_SIZE
        return 0
    return 1


def removeItem():
    global IN, OUT
    if IN != OUT:
        item_removed = BUFFER[OUT]
        BUFFER[OUT] = -1
        OUT = (OUT + 1) % BUFFER_SIZE
        return 0, item_removed
    return 1, 0


def printBuffer():
    myBuffer = ', '.join([str(x) for x in BUFFER])
    print ("Buffer:", myBuffer)


class Producer(Thread):
    def run(self):
        nums = range(5)  # creates list [1,2,3,4]
        global BUFFER
        # empty.acquire(False)
        while True:
            time.sleep(sleepTime)
            num = random.choice(nums)
            lock.acquire()
            if insertItem(num) == 1:
                print("{} waiting!".format(self.getName()))
                # full.acquire()
            else:
                print("{} produced by {}".format(num, self.getName()))
                # empty.release()
            printBuffer()
            lock.release()
            # full.release()


class Consumer(Thread):
    def run(self):
        global BUFFER
        # full.acquire(False)
        while True:
            time.sleep(sleepTime)
            lock.acquire()
            flag, item = removeItem()
            if flag == 1:
                print("{} waiting!".format(self.getName()))
                # empty.acquire()
            else:
                print("{} consumed by {}".format(item, self.getName()))
                # full.release()
            printBuffer()
            lock.release()


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

