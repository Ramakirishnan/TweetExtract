#step 1

import csv
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
url = input("Enter the url of twitter's advance search results page")
driver.get(url)
driver.maximize_window()


tweetlimit = input("How many tweets do you want?")

#step 2

counter = 0
def get_tweet_data(card):
    #print("gettweetdata")
    try:
        postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
    except NoSuchElementException:
        return
    #print("gettweetdata2")
    username = card.find_element_by_xpath('.//span').text
    handle = card.find_element_by_xpath('.//span[contains(text(),"@")]').text
    tweettext = card.find_element_by_xpath('.//div[2]/div[2]/div[2]/div[1]').text
    tweet = (username, postdate, handle, tweettext)
    return tweet


data = []
tweet_ids = set()
last_position = driver.execute_script("return window.pageYOffset;")
scrolling = True

while scrolling:
    page_cards = driver.find_elements_by_xpath('//article[@data-testid="tweet"]')
    for card in page_cards[-15:]:
        tweet = get_tweet_data(card)
        if tweet:
            # print("id data")
            tweet_id = ''.join(tweet)
            if tweet_id not in tweet_ids:
                #print("idnotrepeat")
                print(tweet)
                tweet_ids.add(tweet_id)
                data.append(tweet)
                counter += 1
                #print (counter)
                if counter == int(tweetlimit):
                    scrolling = False
                    break

    scroll_attempt = 0
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        print("done scrolling")
        print(str(counter) + " tweets scraped s0 far")
        sleep(9)
        curr_position = driver.execute_script('return window.pageYOffset;')
        if last_position == curr_position:
            scroll_attempt += 1
            if scroll_attempt >= 7:
                scrolling = False
                break
            else:
                sleep(9)
                print(scroll_attempt)
        else:
            last_position = curr_position
            print("done scraping")
            break

#Step 3

csvname = input("name your csv file") + ".csv"

with open(csvname, 'w', newline='', encoding='utf-8') as f:
    header = ['UserName', 'TimeStamp', 'Handle', 'Tweet']
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)
