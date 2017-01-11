'''
python script which use youtube-dl where each download runs on a thread
'''

import os
import sys
import argparse
from threading import Thread


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

def Create_threadList(NumberLines,url_list):
    # create a thread list
    threads_list = []
    for i in range(NumberLines):
        threads_list.append(Thread(target=youtube_dl, args=(url_list[i],)))
    return threads_list

def youtube_dl(url):
    #runs the youtube-dl command
    os.system('youtube-dl '+url)

def main(pathFile,url_list,file):

    if file:
        #get url from file
        Numberlines = getNumberLines_FromFile(pathFile)
        url_list=getUrl_List_FromFile(pathFile)
        threads_list = Create_threadList(Numberlines,url_list)
        #Run threads
        for i in range(Numberlines):
            threads_list[i].start()
    else:
        #calculate numbers of url in list
        numbers_of_url=len(url_list)
        threads_list= Create_threadList(numbers_of_url,url_list)
        #Run threads
        for i in range(numbers_of_url):
            threads_list[i].start()


if __name__ == "__main__":
    #python runs from command line
    parser = argparse.ArgumentParser(description='Script which use youtube-dl each download runs on a thread')
    parser.add_argument('-a', '--file',help='File path', required=False)
    parser.add_argument('-c', '--url', help='URL List from command line',nargs='+', required=False) #nargs='+' takes one or more arguments
    args=parser.parse_args()
    #get file argument
    pathFile = args.file
    cmd_URL_List =args.url
    if(pathFile):
        #run youtube-dl threads reading url from file
        main(pathFile,"",True)
    if(cmd_URL_List):
        #run youtube-dl threads using url from command line
        main("",cmd_URL_List,False)