#!/usr/bin/python3
from datetime import date
import pandas as pd
import numpy as np
from selenium.webdriver.common.keys import Keys
from selenium import webdriver # driving the actions, links up with the browser
from bs4 import BeautifulSoup
import time
import re
from pick import pick
# import progressbar
import os

import pickle

df = pd.DataFrame(columns=['ID', 'Job Title', 'Organization', 'Division', 'Openings', 'Internal Status', 'City', 'Level',
                           'Applications', 'App Deadline', 'Work Term Duration', "Job Summary", "Job Responsibilities", "Required Skills",
                           "Targeted Degrees and Disciplines", "Application Documents Required"])

login_url = 'https://cas.uwaterloo.ca/cas/login?service=https://waterlooworks.uwaterloo.ca/waterloo.htm'
output_name = 'WW_postings.csv'
choice = 'Applied'
PATH =  r'C:\Users\esthe\Documents\Coding\chromedriver_win32\chromedriver.exe'

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import os

def goToShortlist(driver):
    job_page = "https://waterlooworks.uwaterloo.ca/myAccount/hire-waterloo/full-time-jobs/jobs-postings.htm"
    driver.get(job_page)

    time.sleep(2)
    shortlist_button = driver.find_element(By.CSS_SELECTOR, "#quickSearchCountsContainer > table > tbody > tr:nth-child(2) > td.full > a")
    shortlist_button.click()
    time.sleep(2)

def main():
    # from selenium import webdriver
    # from selenium.webdriver.chrome.options import Options
    # options = Options()
    # options.add_argument("--user-data-dir=C:\\Users\Leon\\Desktop\\Test")
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # driver.get("https://waterlooworks.uwaterloo.ca/waterloo.htm?action=login")


    # input()
    # options = webdriver.ChromeOptions()
    # options.add_argument(r"--user-data-dir=C:\Users\Leon\AppData\Local\Google\Chrome\User Data") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
    # options.add_argument(r'--profile-directory=C:\Users\Leon\AppData\Local\Google\Chrome\User Data\Default') #e.g. Profile 3
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    starting_page = "https://waterlooworks.uwaterloo.ca/waterloo.htm?action=login"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(starting_page) # in original script, this was starting page
    time.sleep(1)
    username_input_field = driver.find_element("id", "userNameInput")
    username_input_field.send_keys("lclyao@uwaterloo.ca")
    username_input_field.submit()
    time.sleep(1)
    password_input_field = driver.find_element("id", "passwordInput")
    password_input_field.send_keys("Vggt+7Q2n#DNv&7")
    password_input_field.submit()
    time.sleep(1)

    auth_button = driver.find_element(By.CSS_SELECTOR, "#auth_methods > fieldset > div.row-label.push-label > button")
    auth_button.click()

    time.sleep(6)

    goToShortlist(driver)

    postings = driver.find_elements(By.XPATH, "//table//tr")[1:]
    
    # first posting

    posting_1 = postings[0]

    cells = posting_1.find_elements(By.TAG_NAME, "td")

    job_name = cells[3].get_attribute('data-totitle')
    company_name = cells[4].get_attribute('data-totitle')

    print(job_name)
    print(company_name)

    apply_button = cells[0].find_element(By.CSS_SELECTOR, "td:nth-child(1) > a.btn.btn-primary.btn-small")

    apply_button.click()

    compile_command = "xelatex -interaction nonstopmode -halt-on-error -file-line-error " \
    "'\\newcommand{\positionnamevalue}{%s} \\newcommand{\companynamevalue}{%s} \input cover_letter'" % (job_name, company_name)
    
    os.system(compile_command)

    copy_command = "sudo cp Cover_letter.pdf /home/leon/Desktop/cover_letter.pdf"

    os.system(compile_command)

    # time.sleep(10)

    time.sleep(6)
    
    upload_button = driver.find_element(By.CSS_SELECTOR, "body > main > div.row-fluid > div > div.panel.panel-default > div.panel-body > div > div > div > div > div.panel-body > a")
    upload_button.click()

    time.sleep(3)
    
    choose_file_button = driver.find_element(By.CSS_SELECTOR, "#fileUpload_docUpload")
    choose_file_button.send_keys("/home/leon/Desktop/cover_letter.pdf")

    time.sleep(1)

    file_name_field = driver.find_element(By.CSS_SELECTOR, "#docName")
    file_name_field.send_keys("%s Cover Letter" % company_name)

    time.sleep(1)

    file_type_dropdown = Select(driver.find_element(By.CSS_SELECTOR, "#docType"))
    file_type_dropdown.select_by_index(1)

    time.sleep(1)

    submit_file_button = driver.find_element(By.CSS_SELECTOR, "#submitFileUploadFormBtn")
    submit_file_button.click()

    time.sleep(1)

    upload_button = driver.find_element(By.CSS_SELECTOR, "body > main > div.row-fluid > div > div.panel.panel-default > div.panel-body > div > div > div > div > div.panel-body > a")
    upload_button.click()

    time.sleep(1)

    file_type_dropdown = Select(driver.find_element(By.CSS_SELECTOR, "#docType"))
    file_type_dropdown.select_by_index(2)

    file_name_field = driver.find_element(By.CSS_SELECTOR, "#docName")
    file_name_field.send_keys("resume")

    choose_file_button = driver.find_element(By.CSS_SELECTOR, "#fileUpload_docUpload")
    choose_file_button.send_keys("/home/leon/Desktop/resume.pdf")

    time.sleep(1)
    submit_file_button = driver.find_element(By.CSS_SELECTOR, "#submitFileUploadFormBtn")
    submit_file_button.click()


    while True:
        os.system(input())

    # print(len(postings))
    # for posting in postings:
        # print(posting.get_attribute('outerHTML'))
        # cells = posting.find_elements(By.TAG_NAME, "td")
        # for cell in cells:
            # print(cell.get_attribute('data-totitle')) 

    # cookies = pickle.load(open("cookies.pkl", "rb"))
    # for cookie in cookies:
    #     driver.add_cookie(cookie)
    # options = uc.ChromeOptions()
    # options.add_argument(f'--user-data-dir=C:\\Users\\Leon\\AppData\\Local\\Google\\Chrome\\User\t Data\\Default') # chrome profile location
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    # options.add_argument('--load-extension=C:\\temp\\plugin-folder')
    # driver = uc.Chrome(options=options)
    # driver.get('https://www.google.com')

    # input()
    # driver.quit()
    # data = get_job_lists(choice, browser, output_name)
    # df.to_csv("WW_raw_postings.csv")

# def get_job_lists(choice, browser, output_name):

#     print("Getting job lists ...")
#     # Navigate to the job listings page then wait for the javascript to load
#     browser.find_element_by_link_text(choice).click()

#     input("Are you ready again?")

#     # Get the HTML of the page and check if this is the last page (next_page_buttons)
#     page_html = browser.execute_script("return document.body.innerHTML")
#     pattern = r'<a href=".+?" onclick="loadPostingTable(.+?)">\s*»\s*<\/a>'
#     next_page_buttons = []
#     next_page_buttons = re.findall(pattern, page_html)

#     # dots for loading screen
#     dots = ""
#     counter_page = 0
#     # Scrape the tables and save it to output_name as a CSV
#     job_posting_importants_order = ['Work Term Duration:', "Job Summary:", "Job Responsibilities:", "Required Skills:",
#                                     "Targeted Degrees and Disciplines:", "Application Documents Required:"]
#     with open(output_name, 'w') as f:
#         row_count = 0
#         job_count = 0
#         while (counter_page < 3):
#             counter_page += 1
#             # loading screen stuff
#             os.system('clear')
#             print("Working" + dots)
#             # update dots
#             if (dots == "..."):
#                 dots = ""
#             else:
#                 dots += "."

#             # wait for JavaScript to load then download the page info
#             time.sleep(2)
#             soup = BeautifulSoup(page_html, "html.parser")

#             for tr in soup.find_all('tr')[2:]: # iterating throw all rows


#                 job_count += 1
#                 print(job_count)
#                 try:
#                     # all the data that was not in the original script
#                     job_posting_importants = {"Work Term Duration:": None, # might need to do some regex filtering
#                                              "Job Summary:" : None,
#                                              "Job Responsibilities:": None,
#                                              "Required Skills:" : None,
#                                              "Targeted Degrees and Disciplines:": None,
#                                              "Application Documents Required:": None}


#                     tds = tr.find_all('td') # iterating all cells in each row.
#                     count = 0
#                     job_info_list = []
#                     for x in tds[0:-1]: # starting with the 3 buttons

#                         if (count == 0): # at 3 buttons
#                             link_container = x.find_all('a')[2]

#                             onclick_link = link_container['onclick']

#                             # clicking the onclick link:
#                             browser.execute_script(onclick_link)
#                             browser.switch_to.window(browser.window_handles[1])

#                             # give the browser 1 seconds for the website to catch up with the code
#                             browser.implicitly_wait(2)

#                             time.sleep(3)
#                             # do stuff, locate the texts of 'job posting importants'

#                             #saving the contents of the html of the new page:
#                             indiv_html = browser.execute_script("return document.body.innerHTML")
#                             indiv_posting = BeautifulSoup(indiv_html, "html.parser")

#                             # finding the third 'table' in the page, as the first table is no use to us

#                             job_posting_information_table = indiv_posting.find_all('table', {'class': 'table-bordered'})[1]

#                             # iterating through all rows in the table
#                             for row in job_posting_information_table.find_all('tr'):
#                                 cell_list = row.find_all('td')
#                                 try:
#                                     key = cell_list[0].get_text().strip()
#                                 except:
#                                     continue


#                                 if (key in job_posting_importants):
#                                     try:
#                                         job_posting_importants[key] = cell_list[1].get_text().strip()
#                                     except:
#                                         job_posting_importants[key] = ""


#                             application_information_table = indiv_posting.find_all('table', {'class': 'table-bordered'})[2]
#                             job_posting_importants["Application Documents Required:"] = application_information_table.find_all('td')[3].get_text().strip()

#                             browser.close() # close current tab
#                             browser.switch_to.window(browser.window_handles[0])

#                         if (count >= 2):
#                             job_info_list.append(str(x.text))

#                         count += 1

#                     for col in job_posting_importants_order:
#                         job_info_list.append(job_posting_importants[col])

#                     df.loc[row_count] = job_info_list
#                     row_count+=1
#                 except:
#                     continue

#             # navigate to the next page and get the HTML, next page buttons
#             next_page_buttons = re.findall(pattern, page_html)
#             browser.find_element_by_link_text("»").click()
#             time.sleep(2)
#             page_html = browser.execute_script("return document.body.innerHTML")



if __name__ == "__main__":
    main()
