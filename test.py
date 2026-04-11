# publisher
import threading
from threading import Condition
import time
import random

class Publisher(threading.Thread):
    def __init__(self, integers, condition: Condition, n):
        threading.Thread.__init__(self)
        self.condition = condition
        self.integers = integers
        self.name = n

    def run(self):
        while True:
            integer = random.randint(0,1000)
            self.condition.acquire() # thread sleeps if this call isn't favorable, if it is, it moves ahead
            print("Condition Acquired by Publisher: {}".format(self.name))
            self.integers.append(integer)
            print(f"Publisher appended: {integer}")
            self.condition.notify() # wakes one thread (n = 1 by default) that's waiting for this condition
            print("Condition Released by Publisher: {}".format(self.name)) # code bet. acquire() & release() is the CRITICAL SECTION.
            self.condition.release()
            time.sleep(1)

# subscriber

class Subscriber(threading.Thread):
    def __init__(self, integers, condition: Condition, n):
        threading.Thread.__init__(self)
        self.integers = integers
        self.condition = condition
        self.name = n

    def run(self):
        while True:
            self.condition.acquire()
            print("Condition Acquired by Consumer: {}".format(self.name))
            while True:
                if self.integers:
                    integer = self.integers.pop()
                    print("{} Popped from list by Consumer: {}".format(integer, self.name))
                    break
                print("Condition Wait by {}".format(self.name))
                self.condition.wait()
            print("Consumer {} Releasing Condition".format(self.name)) # code bet. acquire() & release() is the CRITICAL SECTION.
            self.condition.release()

    # my simpler version of run() which DOES NOT work as well (i was curious about why there's while loops in this code, can't they be tackled by conditions)
    # def run(self):
    #     while True:
    #         self.condition.acquire()
    #         print("Condition Acquired by Consumer: {}".format(self.name))

    #         if self.integers:
    #             integer = self.integers.pop()
    #             print("{} Popped from list by Consumer: {}".format(integer, self.name))
    #         else:
    #             print("Condition Wait by {}".format(self.name))
    #             self.condition.wait()

    #         print("Consumer {} Releasing Condition".format(self.name)) # code bet. acquire() & release() is the CRITICAL SECTION.
    #         self.condition.release()

# why use perpetual while loops instead of just an if condition for critical section?
# ans: I'll answer the subscriber, which has 2 such nested loops.
# 1. outer loop: This one is mandatory because, the thread needs to sustain after a single consume operation. Remove the outer loop, and you'll see that after one pop(), there is no code left for the thread to execute after release. The thread will just.. die. Same reason why we have a while loop in publisher. publisher needs to keep appending elements to array, and not just die after the first append.

# 2. inner loop: this one because of optimization.
# consider case where len(arr) = 1, and publisher woke up > 1 subscribers (maybe n > 1 or it used notify_all()). Let there be 2 threads awake now, A and B. A tries to acquire lock -> succeeds -> checks array and sees element, then pops it -> releases lock & sleeps.... After this, B -> tries to acquire lock -> succeeds -> checks array but no element.. so it hits wait() (meaning it'll wake up on the next notify() call of the publisher). The call eventually comes, and thread B's code starts where it left off.

# now without inner loop, after the wait() returns, B will just release condition for no reason, without ever checking the array... it will take this up the next time it gets the condition...
# with while loop, after wait(), B will restart the while loop and check the array to find a number in it, thus not wasting its chance... This is optimal.

def main():
    integers = []
    condition = threading.Condition()
    # Our Publisher
    pub1 = Publisher(integers, condition, "publisher")
    pub1.start()
    # Our Subscribers
    sub1 = Subscriber(integers, condition, "sub1")
    sub2 = Subscriber(integers, condition, "sub2")
    sub1.start()
    sub2.start()
    ## Joining our Threads
    pub1.join()
    sub1.join()
    sub2.join()

if __name__ == '__main__':
    main()