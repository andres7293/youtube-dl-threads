'''
script de python que usa youtube-dl
donde cada descargar corre en un hilo
'''

import os
import time
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

def youtube_dl(url):
    #runs the youtube-dl command
    os.system('youtube-dl '+url)




path = 'file'
Numberlines = getNumberLines(path)

#assing each url to a list
stream = open(path,mode='r')
counter = 0
url_list =[]
#reading loop
while True:
    line = stream.readline()
    if line:
        #line not empty
        url_list.append(line)
        counter+=1
    else:
        break


# Run threads
for i in range(Numberlines):
    t = Thread(target=youtube_dl, args=(url_list[i],))
    t.start()

