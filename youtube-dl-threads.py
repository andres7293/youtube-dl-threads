'''
script de python que usa youtube-dl
donde cada descargar corre en un hilo
'''

import os
import argparse
from threading import Thread


def getNumberLines(path):
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

def getUrl_List(path):
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

def main(pathFile):

    Numberlines = getNumberLines(pathFile)
    url_list=getUrl_List(pathFile)
    threads_list = Create_threadList(Numberlines,url_list)

    #Run threads
    for i in range(Numberlines):
        threads_list[i].start()

if __name__ == "__main__":
    #python runs from command line
    parser = argparse.ArgumentParser(description='Script which use youtube-dl each download runs on a thread')
    parser.add_argument('-a', '--file',help='File path', required=True)
    args=parser.parse_args()
    #get file argument
    pathFile = args.file
    main(pathFile)