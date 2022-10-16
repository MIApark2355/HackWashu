from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
from collections import Counter

#list and dictionary for hashtags
tag_lst=[]
freq = {}

browser = webdriver.Chrome()
browser.maximize_window()
browser.get("http://www.instagram.com/")

#input user id
user_ID = input("Enter ID: ")
input_ID = WebDriverWait(browser,15).until(EC.presence_of_element_located((By.NAME,"username")))
input_ID.clear()
input_ID.send_keys(user_ID)

#input user pw
user_PW = input("Enter PW: ")
input_PW = WebDriverWait(browser,15).until(EC.presence_of_element_located((By.NAME,"password")))
input_PW.clear()
input_PW.send_keys(user_PW)
input_PW.submit()

time.sleep(8)
browser.get('http://www.instagram.com/'+user_ID+"/")

#method to move to the next post
def to_next(browser):
    b0=WebDriverWait(browser,15).until(EC.presence_of_element_located(((By.CSS_SELECTOR, 'div._aaqg._aaqh'))))
    b0.click()
    time.sleep(3)

#get all the hashtags
def get_hashtags(browser):
    html = browser.page_source
    sp = BeautifulSoup(html,'lxml')
    try:
        content = sp.select('div._a9zr')[0].text
    except:
        content=''

    tags=re.findall(r'#[^\s#,\\]+',content)

    tag=''.join(tags).replace("#"," ")
    tag_data = tag.split()

    for x in tag_data:
        tag_lst.append(x)

    data = [tags]
    return data

time.sleep(5)

#Enter a word to posts and those hashtags
input_word= input("Enter a word: ")
browser.get("http://www.instagram.com/explore/tags/"+str(input_word))
time.sleep(5)

#Moving to the first post
b1=WebDriverWait(browser,15).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div._aagw')))
b1.click()
time.sleep(3)

#Number of posts you want to scrap
num_posts=input("How many posts do you want to check?: ")
results=[]
for i in range(int(num_posts)):
    try:
        data = get_hashtags(browser)
        results.append(data)
        to_next(browser)
    except:
        time.sleep(2)
        to_next(browser)

results_df = pd.DataFrame(results)
results_df.columns=['Hashtags']
results_df.to_excel('hashtags.xlsx')

#method to get the frequency of hashtags
def all_freq(list):
    for x in list:
        if(x!=input_word):
            if (x in freq):
                freq[x] +=1
            else:
                freq[x] = 1
    print()
    print("-------Hashtags Frequency------")
    print("---Search Word:",input_word,"---")
    for k, v in freq.items():
        print(k+' : ' +str(v))
    return freq

#method to get the most frequent tags
def most_freq(list):
    list.remove(input_word) #list without input_word
    c = Counter(list)
    d = c.most_common(1)
    max_num=0
    for k1,v1 in d:
        max_num = v1

    print("---Most Common Hashtags---")
    print("Most common hashtags are used ", max_num, "times.")
    print()
    for k, v in freq.items():
        if(v == max_num):
            print(k + ' : ' + str(v))

all_freq(tag_lst)
print()
most_freq(tag_lst)