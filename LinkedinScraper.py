from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


s = Service("C:/Users/DELL/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=s)



driver.get("https://www.linkedin.com/jobs/search?keywords=&location=United%20States&geoId=103644278&f_JT=V&f_E=2&f_TPR=r86400&f_WT=1&position=1&pageNum=0")
#driver.get("https://www.linkedin.com/jobs/search?keywords=&location=United%20States&geoId=103644278&f_PP=106233382&f_TPR=&f_JT=C&position=1&pageNum=0")
time.sleep(5)

company_names = []
job_role = []
location_details = []
duration = []
links = []



#print(soup.prettify)
driver.find_element_by_xpath("""//*[@id="base-contextual-sign-in-modal"]/div/section/button""").click()
time.sleep(3)

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(6)
    try:

        load_more_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, """//*[@id="main-content"]/section/button"""))
        )
        load_more_button.click()
        time.sleep(3)
    except:
        pass

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


soup = BeautifulSoup(driver.page_source, "lxml")
left_part = soup.find("section",class_="two-pane-serp-page__results-list")
jobs = left_part.find_all("h3",class_="base-search-card__title")
for i in jobs:
    job_role.append(i.text)

cleaned_job_titles = [title.strip().replace("\n", "") for title in job_role]
job_role = cleaned_job_titles


companies = left_part.find_all("a",class_="hidden-nested-link")
for i in companies:
    company_names.append(i.text)
cleaned_company_names = [title.strip().replace("\n","") for title in company_names]
company_names = cleaned_company_names

loc = left_part.find_all("span",class_="job-search-card__location")
for i in loc:
    location_details.append(i.text)
cleaned_location_details = [title.strip().replace("\n","") for title in location_details]
location_details = cleaned_location_details


time = soup.find_all("time",class_="job-search-card__listdate--new")
for  i in time:
    duration.append(i.text)
cleaned_duration = [title.strip().replace("\n","") for title in duration]
duration = cleaned_duration


link = left_part.find_all("a",class_="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]")
for i in link:
    links.append(i.get("href"))



df = pd.DataFrame({"job_title":job_role,"company":company_names,"location":location_details,"link":links})
df.to_csv("linkedin_jobs.csv")
print(df)