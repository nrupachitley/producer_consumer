from __future__ import print_function
from threading import Thread, Lock, Semaphore
import time
import random

lock = Lock()
readlock = Lock()

BUFFER = []
BUFFER_SIZE = 20
full = Semaphore(0)#.acquire()
empty = Semaphore(BUFFER_SIZE)

IN = 0
OUT = 0

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
        OUT = (OUT + 1) % BUFFER_SIZE
        return 0
    return 1


class Producer(Thread):
    def run(self):
        nums = range(5) #creates list [1,2,3,4]
        global BUFFER
        empty.acquire(False)
        #sem_wait(&empty);
        while True:
            time.sleep(sleepTime)
            num = random.choice(nums)
            #print(num)
            lock.acquire()
            if insertItem(num):
                print("Error occured because of Producer")
            else:
                print("Produced", num)
            lock.release()
        full.release()

class Consumer(Thread):
    def run(self):
        global BUFFER
        full.acquire(False)
        while True:
            time.sleep(sleepTime)
            lock.acquire()
            if removeItem():
                print("Error occured because of Consumer")
            else:
                print("Consumed")
            lock.release()
        empty.release()


if __name__ == '__main__':
    sleepTime = input("Insert sleep time for Producer and Consumer threads in seconds: ")
    # numberOfProducers = input("Insert number of Producer threads: ")
    # numberOfConsumers = input("Insert number of Consumer threads: ")


    BUFFER = [0] * BUFFER_SIZE

    threads = []

    #One producer
    myProducer = Producer()
    threads.append(myProducer)

    #One Consumer
    myConsumer = Consumer()
    threads.append(myConsumer)


    # for p in range(numberOfProducers):
    #     myProducer = Producer()    #TODO: Have to edit this call as per Producer functon
    #     threads.append(myProducer)
    #
    # for c in range(numberOfConsumers):
    #     myConsumer = Consumer()    #TODO: Have to edit this call as per Producer functon
    #     threads.append(myConsumer)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    time.sleep(sleepTime)
    print("End")
