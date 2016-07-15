#-*- encoding:utf-8 -*-
import time 
import json
import requests
import os
import codecs

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

content_url = 'https://www.dcard.tw/_api/posts/'
first_comment_url = 'https://www.dcard.tw/f/'
second_comment_url = '/p/'
path = './ids/' 

for dirs , root , files in os.walk(path):
    for filename in files:
        #print filename[:-4]
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

            elem = browser.find_element_by_tag_name("body")

            no_of_pagedown = 200

            while no_of_pagedown:
                elem.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.1)
                no_of_pagedown -= 1

            post_elems = browser.find_elements_by_class_name("CommentEntry_content_1ATrw")

            for comment in post_elems:
                out.write("REPLY %d:\n" % commemt_count)
                out.write(comment.text + "\n")
                commemt_count += 1

            browser.close()
