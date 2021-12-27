import pandas as pd
import configparser as cfg
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

parser = cfg.ConfigParser()
parser.read('config.cfg')
email = parser.get('creds', 'email')
password = parser.get('creds', 'password')

df = pd.read_csv('ids.csv')
ids_ = df.IDs.tolist() # old ids

url = 'https://internshala.com/employer/dashboard'
driver = Chrome()
driver.maximize_window()
driver.implicitly_wait(20)
driver.get(url)

# login page
email_element = driver.find_element(By.ID, 'email')
password_element = driver.find_element(By.ID, 'password')
email_element.send_keys(email)
password_element.send_keys(password)
driver.find_element(By.ID, 'login_submit').click()

time.sleep(10)

ids = [] # new ids
names = []
cities = []
colleges = []
degrees = []
yogs = [] # year pf graduations
emails = []

for id in ids_:
    url = f'https://internshala.com/employer/application_detail/{id}'
    driver.get(url)

    ids.append(id)
    names.append(driver.find_element(By.CLASS_NAME, 'applicant_name').text)
    cities.append(driver.find_element(By.CLASS_NAME, 'applicant_locations').text)
    
    details = driver.find_elements(By.CLASS_NAME, 'line')
    degrees.append(details[0].text)
    colleges.append(details[1].text)
    year = details[2].text
    try:
        yogs.append(year[year.index('-') + 1:].strip())
    except:
        try:
           yogs.append(year[year.index(':') + 1:].strip())
        except:
            yogs.append(year)
    email_element = driver.find_element(By.ID , 'emailContainer')
    emails.append(email_element.find_element(By.TAG_NAME, 'span').text)

driver.close()

dict = {
    'ids': ids,
    'names': names,
    'cities': cities,
    'colleges': colleges,
    'degrees': degrees,
    'yogs': yogs,
    'emails': emails
}
df = pd.DataFrame(dict)
df.to_csv('details.csv', index=False)
