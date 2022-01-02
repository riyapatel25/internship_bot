# selenium stup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from urllib.parse import urlparse
from collections import Counter
import time # to sleep
from time import sleep 

# to find links
from bs4 import BeautifulSoup
import json
import urllib.request
import re

import time # to sleep
import signal


# fill this in with your job preferences!
PREFERENCES = {
    "position_title": "Software Engineering Intern",
    "location": "San Francisco"
}

def signal_handler(signum, frame):
    raise Exception("Timed out!")

# helper method to give user time to log into glassdoor
def login(driver):
    driver.get('https://www.glassdoor.com/index.htm')

    # keep waiting for user to log-in until the URL changes to user page
    while True:
        try:
            WebDriverWait(driver, 1).until(EC.url_contains("member"))
        except TimeoutException:
            break
    return True # return once this is complete

# navigate to appropriate job listing page
def go_to_listings(driver):

    # wait for the search bar to appear
    element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='scBar']"))
        )

    try:
        # look for search bar fields
        position_field = driver.find_element_by_xpath("//*[@id='sc.keyword']")
        location_field = driver.find_element_by_xpath("//*[@id='sc.location']")
        
        # location_field.clear()
        # sleep(4)
        

        # fill in with pre-defined data
        position_field.send_keys(PREFERENCES['position_title'])
        
        length = len(location_field.get_attribute('value'))
        location_field.send_keys(length * Keys.BACKSPACE)
        # location_field.clear()
        sleep(4)
        location_field.send_keys(PREFERENCES['location'])

        # wait for a little so location gets set
        time.sleep(2)
        driver.find_element_by_xpath(" //*[@id='scBar']/div/button").click()
        sleep(6)
        # driver.find_element_by_xpath(" //*[@id='scBar']/div/button").click()
        driver.find_element_by_link_text("See All Jobs").click()
        # print('sucess')


        # close a random popup if it shows up
        try:
            
            driver.find_element_by_xpath("//*[@id='JAModal']/div/div[2]/span").click()
            print('popup error')
        except NoSuchElementException:
            pass

        return True

    # note: please ignore all crappy error handling haha
    except NoSuchElementException:
        print('wrong location')
        return False

# aggregate all url links in a set
def aggregate_links(driver):
    print('start aggregating links')
    allLinks = [] # all hrefs that exist on the page
   
    # wait for page to fully load
    element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='MainCol']/div[1]/ul"))
        )
    # sleep(20)

    time.sleep(5)

    # parse the page source using beautiful soup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source)
    
    # find all hrefs
    allJobLinks = soup.findAll("a", {"class": "jobLink"})
    allLinks = [jobLink['href'] for jobLink in allJobLinks]
    allFixedLinks = []
  

    # clean up the job links by opening, modifying, and 'unraveling' the URL
    for link in allLinks:
        # first, replace GD_JOB_AD with GD_JOB_VIEW
        # this will replace the Glassdoor hosted job page to the proper job page
        # hosted on most likely Greenhouse or Lever
        link = link.replace("GD_JOB_AD", "GD_JOB_VIEW")

        # if there is no glassdoor prefex, add that
        # for example, /partner/jobListing.htm?pos=121... needs the prefix

        if link[0] == '/':
            link = f"https://www.glassdoor.com{link}"
            # print('test 1')
        # then, open up each url and save the result url
        # because we got a 403 error when opening this normally, we have to establish the user agent
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        headers={'User-Agent':user_agent,}
        request=urllib.request.Request(link,None,headers) #The assembled request
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(35)   # Ten seconds
        try:
            # print('in the try')
            # the url is on glassdoor itself, but once it's opened, it redirects - so let's store that
            response = urllib.request.urlopen(request)
            time.sleep(.5)
            newLink = response.geturl()
            print(newLink)
            # if the result url is from glassdoor, it's an 'easy apply' one and worth not saving
            # however, this logic can be changed if you want to keep those
            if "glassdoor" not in newLink and (('greenhouse' in newLink) or ('lever' in newLink)):
                print(newLink)
                print('\n')
                allFixedLinks.append(newLink)
                with open('viable.txt', "a") as f:
                    f.write(newLink + '\n')
        except:
            # horrible way to catch errors but this doesnt happen regualrly (just 302 HTTP error)
            print(f'ERROR: failed for {link}')
            print('\n')
    print('DONE WITH PAGE..')
    sleep(6)
    # convert to a set to eliminate duplicates
    return set(allFixedLinks)

# 'main' method to iterate through all pages and aggregate URLs
def getURLs():
    print('start')
    driver = webdriver.Chrome()
    success = login(driver)
    if not success:
        # close the page if it gets stuck at some point - this logic can be improved
        driver.close()

    success = go_to_listings(driver)
    if not success:
        driver.close()

    allLinks = set()
    page = 1
    # next_url = ''
    while page < 17: # pick an arbitrary number of pages so this doesn't run infinitely
        # print(f'\nNEXT PAGE #: {page}\n')

        # on the first page, the URL is unique and doesn't have a field for the page number
            # aggregate links on first page
            allLinks.update(aggregate_links(driver))
            print('links are agrregated')
            time.sleep(10) # just to give things time
            print('go to next page..')
            driver.find_element_by_xpath("//*[@data-test='pagination-next']").click()
            sleep(6)
            print('on next page')
            # allLinks.update(aggregate_links(driver))
            page+=1
       

            
    list_links = [urlparse(link).hostname for link in list(allLinks)]
    count_list = Counter(list_links)
    print(count_list)
    print('done with ALL links')
    return allLinks

# for testing purpose
# getURLs()
