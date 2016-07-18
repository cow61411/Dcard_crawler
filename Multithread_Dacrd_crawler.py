#-*- encoding:utf-8 -*-
import time 
import json
import requests
import os
import codecs
import threading
import sys
import Queue

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class crawler(threading.Thread):
    def __init__(self , path  , filename):
        threading.Thread.__init__(self)
        self.content_url = 'https://www.dcard.tw/_api/posts/'
        self.first_comment_url = 'https://www.dcard.tw/f/'
        self.second_comment_url = '/p/'
        self.path = path
        #self.data = data
        #self.filename = filename

    def run(self):
        try:
            post_count = 1
            pooldata = threadpool.get()
            data = pooldata[0]
            filename = pooldata[1]
            out = codecs.open(filename[:-4] , 'w' , 'utf8')
            length = len(data)
            for num in data:
                browser = webdriver.Chrome()
                commemt_count = 1

                full_content_url = self.content_url + str(num).strip("\n")
                full_comment_url = self.first_comment_url + filename[:-4] + self.second_comment_url + str(num).strip("\n")
                #print full_content_url
                #print full_comment_url
                print "Crawling forum \"%s\" %d/%d post" % (filename[:-4] , post_count , length)
                res = requests.get(full_content_url)
                content = json.loads(res.text)

                out.write("POST %d:\n" % post_count)
                post_count += 1
                if content.has_key('content'):
                    out.write(content['content'] + "\n")

                browser.get(full_comment_url)
                time.sleep(0.2)
                lastHeight = browser.execute_script("return document.body.scrollHeight")
                while True:
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(0.5)
                    newHeight = browser.execute_script("return document.body.scrollHeight")
                    if newHeight == lastHeight:
                        break
                    lastHeight = newHeight
                post_elems = browser.find_elements_by_class_name("CommentEntry_content_1ATrw")

                for comment in post_elems:
                    out.write("REPLY %d:\n" % commemt_count)
                    out.write(comment.text + "\n")
                    commemt_count += 1

                browser.close()
            threadpool.task_done()
        except:
            pass


if __name__ == "__main__":
    threads = []
    path = './ids/'
    count = 1
    threadpool = Queue.Queue(0)
    for dirs , root , files in os.walk(path):
        for filename in files:
            #if count < 10:
            #for i in xrange(10):
            temp = []
            data =  open(path + filename , 'r').readlines()
            temp.append(data)
            temp.append(filename)
            threadpool.put(temp)
                #thread = crawler('./ids/' , data , filename) 
                #thread.start()
                #threads.append(thread)
            #count += 1
            #print filename
    for i in xrange(10):
        thread = crawler('./ids/' , filename) 
        thread.start()
        threads.append(thread)


    #for thread in threads:
        #thread.join()
    threadpool.join()
            #print filename[:-4]
    '''
            out = codecs.open(filename[:-4] , 'w' , 'utf8')
            post_count = 1
            for num in open(path + filename , 'r').readlines():
                browser = webdriver.Chrome()
                commemt_count = 1

                full_content_url = content_url + str(num).strip("\n")
                full_comment_url = first_comment_url + filename[:-4] + second_comment_url + str(num).strip("\n")
                print full_content_url
                #print full_comment_url
                data = requests.get(full_content_url)
                content = json.loads(data.text)

                out.write("POST %d:\n" % post_count)
                post_count += 1
                if content.has_key('content'):
                    out.write(content['content'] + "\n")

                browser.get(full_comment_url)
                time.sleep(0.2)
                lastHeight = browser.execute_script("return document.body.scrollHeight")
                while True:
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(0.5)
                    newHeight = browser.execute_script("return document.body.scrollHeight")
                    if newHeight == lastHeight:
                        break
                    lastHeight = newHeight
                post_elems = browser.find_elements_by_class_name("CommentEntry_content_1ATrw")

                for comment in post_elems:
                    out.write("REPLY %d:\n" % commemt_count)
                    out.write(comment.text + "\n")
                    commemt_count += 1

                browser.close()
            '''


