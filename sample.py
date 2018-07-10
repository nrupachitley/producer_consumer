from __future__ import print_function
from threading import Thread, Lock, Semaphore
import time

lock = Lock()
readlock = Lock()

BUFFER = []
BUFFER_SIZE = 20
full = Semaphore(0)
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
#   TODO: Have to complete this part


class Consumer(Thread):
    def run(self):
#   TODO: Have to complete this part


if __name__ == '__main__':
    sleepTime = input("Insert sleep time for Producer and Consumer threads in seconds: ")
    numberOfProducers = input("Insert number of Producer threads: ")
    numberOfConsumers = input("Insert number of Consumer threads: ")


    BUFFER = [0] * BUFFER_SIZE
    for p in range(numberOfProducers):
        myProducer = Producer()    #TODO: Have to edit this call as per Producer functon
        myProducer.start()
    for c in range(numberOfConsumers):
        myConsumer = Consumer()    #TODO: Have to edit this call as per Producer functon
        myConsumer.start()


    time.sleep(sleepTime)
    print("End")

