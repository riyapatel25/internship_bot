from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os # to get the resume file
import time # to sleep
from time import sleep 
import get_links
import pynput
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller
from tkinter import messagebox
import pyautogui, sys

#helpers
def fill_slot(driver, slot_name, value):
    try:
        slot = driver.find_element_by_id(slot_name)
        slot.clear()
        slot.send_keys(value)
    except:
        pass

def fill_dropdown(driver, slot_name, value):
    try:
        loc = driver.find_element_by_id(slot_name)
        sleep(2)
        loc.send_keys(value)
        sleep(1)
        loc.send_keys(Keys.DOWN) # manipulate a dropdown menu
        sleep(.4)
        loc.send_keys(Keys.RETURN)
    except:
        pass

def fill_special_dropdown_school(driver, slot_name):
    try:
        loc = driver.find_element_by_link_text(slot_name)
        loc.click()
        keyboard = Controller()
        keyboard.type('University of Waterloo')
        sleep(2)
        kb = Controller()
        kb.press(Key.tab)
        kb.release(Key.tab)
        time.sleep(.5) # give user time to manually input if this fails
    except:
        pass
def fill_special_dropdown_degree(driver, slot_name):
    try:
        loc = driver.find_element_by_link_text(slot_name)
        loc.click()
        keyboard = Controller()
        keyboard.type('Ba')
        sleep(2)
        kb = Controller()
        kb.press(Key.tab)
        kb.release(Key.tab)
        time.sleep(.5) # give user time to manually input if this fails
    except:
        pass  
def fill_special_dropdown_discipline(driver, slot_name):
    try:
        loc = driver.find_element_by_link_text(slot_name)
        loc.click()
        keyboard = Controller()
        # sleep(1)
        keyboard.type('Computer Science')
        sleep(2)
        # sleep(1)
        kb = Controller()
        kb.press(Key.tab)
        kb.release(Key.tab)
        time.sleep(.5) # give user time to manually input if this fails
    except:
        pass 

#helpers

# Fill in this dictionary with your personal details!
f_name = 'Riya'
l_name = "Patel"
email = 'riyap7521@gmail.com'
phone = '7145896115'
location = 'San Francisco'
uni = 'University of Waterloo'
degree = 'Bachelor\'s Degree'
start_m = '09'
start_y = '2021'
end_m = '05'
end_y = '2026'
discipline = 'Software Engineering'
title = "N/A"
linkedin = "https://www.linkedin.com/in/riya-patel-5709031b3"
website_port = "https://riyapatel25.github.io/"
company="N/A"
github="https://github.com/riyapatel25"

#GREENHOUSE HELPER
def greenhouse(driver):
    # basic info
    driver.find_element_by_id('first_name').send_keys(f_name)
    driver.find_element_by_id('last_name').send_keys(l_name)
    try:
        driver.find_element_by_id('email').send_keys(email)
        driver.find_element_by_id('phone').send_keys(phone)
    except:
        pass

    # Attach resume
    # print('trying to attach resume...')
    target = driver.find_element_by_link_text('Attach')
    target.click()

    #CLICK desktop
    pyautogui.moveTo(252, 132)
    pyautogui.click() 
    #CLICK aaa folder
    pyautogui.moveTo(392, 76)
    pyautogui.click() 
    #CLICK open
    pyautogui.moveTo(1209, 358)
    pyautogui.click() 
    #CLICK pdf
    pyautogui.moveTo(428, 75)
    pyautogui.click() 
    #CLICK open
    pyautogui.moveTo(1209, 358)
    pyautogui.click() 

    # add location
    fill_dropdown(driver, 'job_application_location', location)
    # add dates for grad/company. note if its company the dates will be your grad dates
    driver.find_element_by_class_name('start-date-month').send_keys(start_m)
    driver.find_element_by_class_name('start-date-year').send_keys(start_y)
    driver.find_element_by_class_name('end-date-month').send_keys(end_m)
    driver.find_element_by_class_name('end-date-year').send_keys(end_y)

    #school
    try:
        fill_special_dropdown_school(driver, 'Select a School')
    except:
        pass
     #degree
    try:
        fill_special_dropdown_degree(driver, 'Select a Degree')
    except:
        pass
     #discipline
    try:
        fill_special_dropdown_discipline(driver, 'Select a Discipline')
    except:
        pass
    
    # messagebox.showinfo(title='Waiting for you', message='Finish on screen app, submit, then click OK.')
    print('Finish app')
    val = int(input("Enter 1 when you are done, Enter 2 to pass "))
    if val == 1:
        driver.find_element_by_id("submit_app").click()
    elif user_val == 2:  
        pass

# LEVER HELPER
def lever(driver):
    # navigate to the application page
    driver.find_element_by_class_name('template-btn-submit').click()
    # print('on app page')
    target = driver.find_element_by_link_text('ATTACH RESUME/CV')
    target.click()
    # print('resume butt clicked')

    #CLICK desktop
    pyautogui.moveTo(249, 130)
    pyautogui.click() 
    #CLICK aaa folder
    pyautogui.moveTo(392, 76)
    pyautogui.click() 
    #CLICK open
    pyautogui.moveTo(1197, 355)
    pyautogui.click() 
    #CLICK pdf
    pyautogui.moveTo(392, 76)
    pyautogui.click() 
    #CLICK open
    pyautogui.moveTo(1197, 355)
    pyautogui.click() 

    # basic info
    driver.find_element_by_name('name').send_keys(f_name + ' ' + l_name)
    driver.find_element_by_name('email').send_keys(email)
    try:
        driver.find_element_by_name('phone').send_keys(phone)
    except:
        pass
    field = driver.find_element_by_name('org')
    length = len(field.get_attribute('value'))
    field.send_keys(length * Keys.BACKSPACE)
    field.send_keys(company)
    
    # socials
    #linkedin
    try:
        driver.find_element_by_name('urls[LinkedIn]').send_keys(linkedin)
    except:
        pass
    #github
    try:
        driver.find_element_by_name('urls[GitHub]').send_keys(github)
    except:
        pass
    #website portfolio
    try:
        driver.find_element_by_name('urls[Portfolio]').send_keys(website_port)
    except:
        pass

    # add university
    try:
        driver.find_element_by_class_name('application-university').click()
        search = driver.find_element_by_xpath("//*[@type='search']")
        search.send_keys(uni) # find university in dropdown
        search.send_keys(Keys.RETURN)
    except:
        pass

    # add how you found out about the company
    try:
        driver.find_element_by_xpath('//input[@value="Job Site (i.e. Glassdoor, Indeed)"]').click()
    except NoSuchElementException:
        pass

    # messagebox.showinfo(title='Waiting for you', message='Finish on screen app, submit, then click OK.')
    print('Finish app')
    val = int(input("Enter 1 when you are done, Enter 2 to pass "))
    if val == 1:
        # driver.find_element_by_id("submit_app").click()
        # driver.find_element_by_link_text("Submit application").click()
        # driver.find_element_by_xpath("//input[@type='submit']").click()
        driver.find_element_by_xpath("//*[@type='submit']").click()
    elif user_val == 2:  
        pass

#MAIN
if __name__ == '__main__':
    print('main')
    user_val = int(input("Enter 1 for scraping, 2 if already scraped and viable.txt has contents: "))

    # call get_links to automatically scrape job listings from glassdoor
    if user_val == 1:
        print('user chose 1')
        aggregatedURLs = get_links.getURLs() #get links into viable.txt->call get_links 
    elif user_val == 2: #start applying 
        print('user chose 2')
        f = open('viable.txt', 'r').read().splitlines()
        # clean up viable txt file, delete repeats
        aggregatedURLs = set(f)#sets don't have duplicates
        with open('viable.txt', 'w') as f1:
            for link in aggregatedURLs:
                f1.write("%s\n" % link)
    #print clean urls in aggregatedURLS
    print(f'Job Listings: {aggregatedURLs}')
    print('\n')

    chrome_path = r'/usr/local/bin/chromedriver' #path from 'which chromedriver'
    driver = webdriver.Chrome(executable_path=chrome_path)
    driver.maximize_window()
    for url in aggregatedURLs:
        print('\n')
    #GREENHOUSE URLS 
        if 'greenhouse' in url:
            driver.get(url)
            try:
                greenhouse(driver) #call function to apply 
                print(f'SUCCESS FOR: {url}')
                #once applied->add to applied.txt file
                with open('applied.txt', "a") as f:
                    f.write(url + '\n')
            except Exception:
                print(f"FAILED FOR {url}")
                continue
            sleep(3)
    #LEVER URLS
        elif 'lever' in url:
            driver.get(url)
            try:
                lever(driver)#call function to apply
                print(f'SUCCESS FOR: {url}')
                #once applied->add to applied.txt file
                with open('applied.txt', "a") as f:
                    f.write(url + '\n')
            except Exception as e:
                print(f"FAILED FOR {url}")
                print(e)
                continue
            sleep(3)


        # time.sleep(2.33) # can lengthen this as necessary (for captcha, for example)

    driver.close()
