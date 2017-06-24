from threading import Thread
import os
import sys

class youtube_dl_scheduler:

    def __init__(self,url_list):
        self.url_list=url_list
        self.thread_list = []
        self.counter = 0
        self.url_list_len = len(url_list)
        print("DEBUG: url list len = "+str(self.url_list_len))

    def youtube_dl(self,url):
        os.system('youtube-dl '+url)

    def create_thread_list(self,numbers_of_threads):
        for i in range(numbers_of_threads):
            self.thread_list.append(Thread(target=self.youtube_dl, args=(self.url_list[i],)))

        #increment counter to number of thread_list
        self.counter = numbers_of_threads

    def scheduler_loop(self):
        while (self.counter < self.url_list_len):
            #iterate over thread list checking when a thread die
            for i in range(len(self.thread_list)):
                if(not self.thread_list[i].isAlive()):
                    print('DEBUG: Thread '+str(i)+ ' has died')
                    print('DEBUG: Counter = '+str(self.counter))
                    #thread died
                    #add other thread
                    self.thread_list[i]=Thread(target=self.youtube_dl, args=(self.url_list[self.counter],))
                    #start thread
                    self.thread_list[i].start()
                    #check if
                    if(self.counter < self.url_list_len):
                        self.counter = self.counter + 1
                    else:
                        #no more downloads
                        #set counter to end of url list
                        self.counter = self.url_list_len -1
                        break
        print("All download has finished")
        print(str(len(self.thread_list))+' Threads used')
        print(str(len(self.url_list))+' videos downloaded')

    def start_threads(self,number_of_threads):
        for i in range(number_of_threads):
            self.thread_list[i].start()

url_list = []
url_list.append('https://www.youtube.com/watch?v=NZ6V63u_-D8')
url_list.append('https://www.youtube.com/watch?v=rNQCFBEHxms')
url_list.append('https://www.youtube.com/watch?v=GIj6DpC4B6g')
url_list.append('https://www.youtube.com/watch?v=oP0lX4pG9T0')

n=2

yt = youtube_dl_scheduler(url_list)
yt.create_thread_list(n)
yt.start_threads(n)
yt.scheduler_loop()
