'''
python script which use youtube-dl where each download runs on a thread
'''

import os
import sys
import argparse
import timeit
from threading import Thread

class youtube_dl_scheduler:

    def __init__(self,number_of_threads,url_list):
        self.url_list=url_list
        self.number_of_threads = number_of_threads
        #pointer to keep trace the next download
        self.counter = 0
        #create thread list object
        self.thread_list = []
        self.url_list_len = len(url_list)
        print("Number of downloads = "+str(self.url_list_len))
        print("Number of threads   = "+str(self.number_of_threads))

    def _youtube_dl(self,url):
        #call system youtube-dl
        os.system('youtube-dl '+url +'> /dev/null 2>&1')

    def _create_thread_list(self):
        #create thread list, associate it with youtube_dl and assign url to them
        for i in range(self.number_of_threads):
            self.thread_list.append(Thread(target=self._youtube_dl, args=(self.url_list[i],)))

    def _start_threads(self):
            for i in range(self.number_of_threads):
                self.thread_list[i].start()
            #set counter to point where, not downloaded url
            self.counter = self.number_of_threads

    def _download_loop(self):
        #iterate over thread list checking when a thread die
        for i in range(len(self.thread_list)):
            #check if thread has died
            if(not self.thread_list[i].isAlive()):
                #thread died
                print('DEBUG: Thread '+str(i)+ ' has died')
                print('DEBUG: Counter = '+str(self.counter))
                #create other thread on the same index of died thread
                self.thread_list[i]=Thread(target=self._youtube_dl, args=(self.url_list[self.counter],))
                #start thread
                self.thread_list[i].start()
                #check if end of url list
                if(self.counter < self.url_list_len - 1):
                    #url list have more items
                    #increment counter
                    self.counter = self.counter + 1
                    return False
                else:
                    #no more downloads
                    return True

    def start(self):
        #measure download time
        start = timeit.timeit()
        finished = False
        self._create_thread_list()
        self._start_threads()
        #scheduler loop
        try :
            while (not finished):
                finished=self._download_loop()

            print("All download has finished")
            end = timeit.timeit()
            print("Download time = "+ str(end-start)+' secs\n\r')
        except KeyboardInterrupt:
            print("EXIT")
            sys.exit()

def main(pathFile,url_list,number_of_threads,file):

    if file:
        #get url from file
        url_list=getUrl_List_FromFile(pathFile)
        yt_sch = youtube_dl_scheduler(number_of_threads,url_list)
        yt_sch.start()
    else:
        #url provided by cli
        #create scheduler class
        yt_sch = youtube_dl_scheduler(number_of_threads,url_list)
        yt_sch.start()

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
