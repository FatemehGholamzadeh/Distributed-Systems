import threading
from scripts.judge import judgement
from coders.models import UserProfile
from scripts.judge2 import evaluate

numberOfThreads = int(len(UserProfile.objects.all()) /3)

class myThread (threading.Thread):

    def __init__(self, threadID, name,csub):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.csub = csub

    def run(self):
        print("Starting " + self.name)
        evaluate(self.csub)
        print("Exiting " + self.name)


def start_judging(numberOfThreads):
    for i in range(numberOfThreads):
        thread = myThread(i,"Thread-"+str(i))
        thread.start()
    print("\nExiting Main Thread")

# start_judging(numberOfThreads)

