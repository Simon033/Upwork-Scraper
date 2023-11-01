from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import csv
from csv import writer

chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors')

#change keyword as per need
keyword = 'python'

# url to search for lates projects in upwork with the keyword as search key
url = f'https://www.upwork.com/nx/jobs/search/?q={keyword}&sort=recency'

# initialize a selenium webdriver
driver = webdriver.Chrome(options=chrome_options,)

driver.get(url)

time.sleep(2)

counter = 0


#open document and start writing
csv_filename='UpworkData.csv'
with open(csv_filename,'a', newline='') as fd:
    csv_file= writer(fd, delimiter=",")

    # write column labels
    csv_file.writerow(['Job Title','Pay','Contractor Tier','Url'])

    while True:

        # wait content to be loaded
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h2[class='my-0 p-sm-right job-tile-title'] > a")))

        # take web element
        job_title = driver.find_elements(By.CSS_SELECTOR, "h2[class='my-0 p-sm-right job-tile-title'] > a")
        job_pay = driver.find_elements(By.CSS_SELECTOR, "strong[data-test='job-type']")
        contractor_tier = driver.find_elements(By.CSS_SELECTOR, "span[data-test='contractor-tier']")
        job_url = driver.find_elements(By.CSS_SELECTOR, "h2[class='my-0 p-sm-right job-tile-title'] > a")
        
        # write each entry of data to a row
        for i in range(len(job_title)):
            csv_file.writerow([
                job_title[i].text,
                job_pay[i].text,
                contractor_tier[i].text,
                job_url[i].get_attribute('href')
                ])
            
        # specify page limit to break
        if (counter == 4):
            break          
        
        # detect next button
        nextButton = driver.find_elements(By.CSS_SELECTOR, "button[class='up-pagination-item up-btn up-btn-link'] > div[class='next-icon up-icon']")
        
        # move to next page
        nextButton[0].click()
        time.sleep(2)

        counter += 1
        print('page: ' + str(counter))
        
# Close the WebDriver
driver.quit()
print(f'Task Completed, file saved as {csv_filename}')