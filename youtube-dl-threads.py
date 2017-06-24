'''
python script which use youtube-dl where each download runs on a thread
'''

import os
import sys
import argparse
from threading import Thread

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


def getNumberLines_FromFile(path):
    #gets the numbers of lines that file have
    stream = open(path,mode='r')
    counter = 0
    #reading loop
    while True:
        line = stream.readline()
        if line:
            #line not empty
            counter+=1
        else:
            break
    stream.close()
    return counter

def getUrl_List_FromFile(path):
    # assing each url to a list
    stream = open(path, mode='r')
    counter = 0
    url_list = []
    # reading loop
    while True:
        line = stream.readline()
        if line:
            # line not empty
            url_list.append(line)
            counter += 1
        else:
            break
    stream.close()
    return url_list

def main(pathFile,url_list,number_of_threads,file):

    if file:
        #get url from file
        Numberlines = getNumberLines_FromFile(pathFile)
        url_list=getUrl_List_FromFile(pathFile)
        yt_sch = youtube_dl_scheduler(url_list)
        #create scheduler class
        yt_sch.create_thread_list(number_of_threads)
        yt_sch.start_threads(number_of_threads)
        yt_sch.scheduler_loop()
    else:
        #calculate numbers of url in list
        #create scheduler class
        yt_sch = youtube_dl_scheduler(url_list)
        yt_sch.create_thread_list(number_of_threads)
        yt_sch.start_threads(number_of_threads)
        yt_sch.scheduler_loop()

if __name__ == "__main__":
    #python runs from command line
    parser = argparse.ArgumentParser(description='Script which use youtube-dl each download runs on a thread')
    parser.add_argument('-a', '--file',help='File path', required=False)
    parser.add_argument('-c', '--url', help='URL List from command line',nargs='+', required=False) #nargs='+' takes one or more arguments
    parser.add_argument('-n', '--threads', help='Number of threads to run', required=False)
    args=parser.parse_args()
    #get command line arguments
    pathFile = args.file
    cmd_URL_List =args.url
    number_of_threads = args.threads
    if(not number_of_threads):
        number_of_threads=2#default number of threads
    else:
        number_of_threads = int(args.threads)
    if(pathFile):
        #run youtube-dl threads reading url from file
        main(pathFile,"",number_of_threads,True)
    if(cmd_URL_List):
        #run youtube-dl threads using url from command line
        main("",cmd_URL_List,number_of_threads,False)
