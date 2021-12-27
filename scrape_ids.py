import pandas as pd
import configparser as cfg
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

parser = cfg.ConfigParser()
parser.read('config.cfg')
email = parser.get('creds', 'email')
password = parser.get('creds', 'password')

url = 'https://internshala.com/employer/dashboard'
driver = Chrome()
driver.maximize_window()
driver.implicitly_wait(15)
driver.get(url)

# login page
email_element = driver.find_element(By.ID, 'email')
password_element = driver.find_element(By.ID, 'password')
email_element.send_keys(email)
password_element.send_keys(password)
driver.find_element(By.ID, 'login_submit').click()

# logged in
driver.find_element(By.CLASS_NAME, 'application_count').click()

driver.find_element(By.ID, 'hired_applications').click()

applications_opened = driver.find_elements(By.XPATH, '//div[@class="individual_application individual_application_hired opened_application  "]')
applications_unopened = driver.find_elements(By.XPATH, '//div[@class="individual_application individual_application_hired unopened_application  "]')

while True:
    print(len(applications_opened) + len(applications_unopened))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1.5)
    new_applications_opened = driver.find_elements(By.XPATH, '//div[@class="individual_application individual_application_hired opened_application  "]')
    new_applications_unopened = driver.find_elements(By.XPATH, '//div[@class="individual_application individual_application_hired unopened_application  "]')
    if len(new_applications_opened) + len(new_applications_unopened) > len(applications_opened) + len(applications_unopened):
        applications_opened = new_applications_opened
        applications_unopened = new_applications_unopened
    else:
        break

ids = []

for application in applications_opened:
    id = application.get_attribute('id')
    ids.append(id[id.rindex('_') + 1:])

for application in applications_unopened:
    id = application.get_attribute('id')
    ids.append(id[id.rindex('_') + 1:])

print()
print(len(ids))
print(ids)

driver.close()

dict = {'IDs': ids}
df = pd.DataFrame(dict)
df.to_csv('ids.csv', index=False)
