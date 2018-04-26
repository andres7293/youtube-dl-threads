import threading
import time
import os
import argparse

class youtube_dl_thread:
    def __init__(self, number_of_threads=1):
        self.number_of_threads = number_of_threads
        self.thread_list = []
        self.__init_thread_pool()

    def __youtube_dl(self, url):
        os.system('youtube-dl -q ' + url)

    def download_by_list(self, url_list):
        for url in url_list:
            while not self.add_dl_to_pool(url):
                time.sleep(1)
        #wait until all dl finish
        while self.get_number_of_occupied_threads() > 0:
            time.sleep(1)

    def download_by_file(self, path):
        with open(path, 'r') as file:
            url = file.readline()
            while url:
                if not self.add_dl_to_pool(url):
                    time.sleep(1)
                else:
                    url = file.readline()
        #wait pending dl to finish
        while self.get_number_of_occupied_threads() > 0:
            time.sleep(1)

    def __init_thread_pool(self):
        for i in range(self.number_of_threads):
            thread = threading.Thread()
            self.thread_list.append(thread)

    def add_dl_to_pool(self, url):
        for i in range(self.number_of_threads):
            if not self.thread_list[i].is_alive():
                thread = threading.Thread(target=self.__youtube_dl, args=(url, ))
                self.thread_list[i] = thread
                self.thread_list[i].start()
                return True
        return False

    def get_number_of_free_threads(self):
        free = 0
        for i in range(self.number_of_threads):
            if not self.thread_list[i].is_alive():
                free = free + 1
        return free
    
    def get_number_of_occupied_threads(self):
        occupied = 0
        for i in range(self.number_of_threads):
            if self.thread_list[i].is_alive():
                occupied = occupied + 1
        return occupied


if __name__ == '__main__':
    #is running by cli
    parser = argparse.ArgumentParser(description='Script which use youtube-dl each download runs on a thread')
    parser.add_argument('-a', '--file', help='File path', required=False)
    parser.add_argument('-c', '--url', help='URL List from command line', nargs='+', required=False) #nargs='+' takes one or more arguments
    parser.add_argument('-n', '--threads', help='Number of threads to run', required=False)
    args=parser.parse_args()
    #get command line arguments
    path = args.file
    url_list = args.url
    number_of_threads = int(args.threads)
    youtube_dl = youtube_dl_thread(number_of_threads)
    if number_of_threads and url_list:
        youtube_dl.download_by_list(url_list)
    elif (number_of_threads and path):
        youtube_dl.download_by_file(path)
