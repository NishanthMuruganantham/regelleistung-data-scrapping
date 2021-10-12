from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import datetime
import time
import os
import pytz


base_url = "https://www.regelleistung.net/ext/data/?lang=en"
chrome_driver = os.path.join(os.path.dirname(__file__),"chromedriver.exe")
download_folder = os.path.join(os.path.dirname(__file__),"downloaded_files")

chrome_path = r"D:\Program Files\Google\Chrome\Application\chrome.exe"

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
yesterday = yesterday.strftime("%d.%m.%Y")

options = Options()
#options.headless = True
options.binary_location = chrome_path
prefs = {'download.default_directory' : download_folder}
options.add_experimental_option('prefs', prefs)
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(chrome_driver, options = options)
driver.implicitly_wait(20)
driver.get(base_url)
driver.maximize_window()


time.sleep(2)
fill_from_date = driver.find_element_by_xpath("//div[contains(@class,'input-group input-group-sm date')]/input[contains(@id,'from-date')]")
fill_from_date.send_keys(Keys.CONTROL, 'a')
fill_from_date.send_keys(Keys.CONTROL, 'x')
fill_from_date.send_keys(yesterday)

enable_download = driver.find_element_by_id("form-download")
enable_download.click()

time.sleep(2)
tso_dropdown = driver.find_element_by_name("tsoId")
tso_dropdown.click()

tso_dropdown_option_xpath = "//div[contains(@class,'input-group input-group-sm')]/select[contains(@name,'tsoId')]/option"
tso_dropdown_options = driver.find_elements_by_xpath(tso_dropdown_option_xpath)

for i in range(1, len(tso_dropdown_options) + 1):
    time.sleep(2)
    select_tso_option = driver.find_element_by_xpath(f"({tso_dropdown_option_xpath})[{i}]")
    select_tso_option.click()
    
    time.sleep(2)
    data_type_dropdown = driver.find_element_by_name("dataType")
    data_type_dropdown.click()
    
    data_type_options_xpath = "//div[contains(@class,'input-group input-group-sm')]/select[contains(@name,'dataType')]/option"
    data_type_options = driver.find_elements_by_xpath(data_type_options_xpath)
    
    for j in range(1, len(data_type_options) + 1):
        time.sleep(2)
        select_datatype_option = driver.find_element_by_xpath(f"({data_type_options_xpath})[{j}]")
        select_datatype_option.click()
        
        download = driver.find_element_by_id("submit-button")
        download.click()
    
    
time.sleep(3)

driver.close()
driver.quit()


