import threading
from scripts.judge import judgement
from coders.models import UserProfile

numberOfThreads = int(len(UserProfile.objects.all()) /3)

class myThread (threading.Thread):

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("Starting " + self.name)
        judgement(self.threadID,numberOfThreads)
        print("Exiting " + self.name)


def start_judging(numberOfThreads):
    for i in range(numberOfThreads):
        thread = myThread(i,"Thread-"+str(i))
        thread.start()
    # Create new threads
    # thread0 = myThread(0,"Thread-0")
    # thread1 = myThread(1, "Thread-1")
    # thread2 = myThread(2, "Thread-2")
    #
    # # Start new Threads
    # thread0.start()
    # thread1.start()
    # thread2.start()

    print("\nExiting Main Thread")

start_judging(numberOfThreads)

