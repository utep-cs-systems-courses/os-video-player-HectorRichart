import threading


class Queue:
    def __init__(self):
        self.queue = []
        self.size = 0
        self.active = True
        #Semaphores help us to avoid leading a race condition where two processes could try to access 
        #the same resource

        #mutex lock help us to protect the queue, in this case we dont want a process reading the queue and another one trying to write to it 
        self.lock = threading.Lock()
        self.full = threading.Semaphore(0) #filling semaphore (resources)
        self.empty = threading.Semaphore(10) #limit of resources (will be decrementing as we add frames)

    #adds item to semaphore resources, takes the lock and after done it releases the lock
    def enqueue(self, item):
        self.empty.acquire() #acquires a resource so the 10 is decremented 
        self.lock.acquire()
        self.queue.append(item)
        self.lock.release() #release the lock
        self.full.release() #release the resource taken

    #takes a resource for frame at position 0, takes the lock and then when done releases the resource it was using 
    def deque(self):
        self.full.acquire()
        self.lock.acquire()
        item = self.queue.pop(0)
        self.lock.release()
        self.empty.release() 
        return item

    def isEmpty(self):
        self.lock.acquire()
        retVal = len(self.queue) == 0
        self.lock.release()
        return retVal

    def kill(self):
        self.active = False

    def isActive(self):
        return self.active
