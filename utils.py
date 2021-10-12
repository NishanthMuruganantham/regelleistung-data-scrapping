from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import pandas as pd
import datetime
import logging
import time
import glob
import os


scrap_logger = logging.getLogger("Data Scrapping")
merge_logger = logging.getLogger("Merging Files")
chrome_path = r"D:\Program Files\Google\Chrome\Application\chrome.exe"

def download_csv_files(base_url, chrome_driver, download_folder):
    
    """
    [download_csv_files]
        - it will go to https://www.regelleistung.net/ext/data/?lang=en and will select the apprpriate dropdowns and extract the table data
        - Here, the code will not DIRECTLY DOWNLOAD THE FILE . Instead, it will scrap the data present in the Web UI
        - if downloaded the file directly using provided download option, the file contains unordered and garbage data
    """
    
    file_count = 1
    driver = None
    try:
        for f in os.listdir(download_folder):
            os.remove(os.path.join(download_folder, f))
        print("file downloading started. It will take some time to download all the files. Please monitor the progress in LogFile.log")
        
        #* finding yesterday date
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        yesterday = yesterday.strftime("%d.%m.%Y")
        
        #* configuring driver options
        options = Options()
        options.headless = True
        options.binary_location = chrome_path
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        #* setting up driver
        driver = webdriver.Chrome(chrome_driver, options = options)
        driver.implicitly_wait(20)
        driver.get(base_url)
        scrap_logger.info("URL is opened")
        driver.maximize_window()
        time.sleep(2)
        
        #* filling from date
        fill_from_date = driver.find_element_by_xpath("//div[contains(@class,'input-group input-group-sm date')]/input[contains(@id,'from-date')]")
        fill_from_date.send_keys(Keys.CONTROL, 'a')
        fill_from_date.send_keys(Keys.CONTROL, 'x')
        fill_from_date.send_keys(yesterday)
        scrap_logger.info("filled from date")
        
        #* clicking TSO dropdown
        tso_dropdown = driver.find_element_by_name("tsoId")
        tso_dropdown.click()
        scrap_logger.info("tso dropdown clicked")
        
        #* finding total available TSO options
        tso_dropdown_option_xpath = "//div[contains(@class,'input-group input-group-sm')]/select[contains(@name,'tsoId')]/option"
        tso_dropdown_options = driver.find_elements_by_xpath(tso_dropdown_option_xpath)
        scrap_logger.info(f"Total TSO options = {len(tso_dropdown_options)}")
        time.sleep(1)
        
        #* going through each and every available TSO options one by one
        scrap_logger.info("going through each and every available TSO options one by one")
        for i in range(1, len(tso_dropdown_options) + 1):
            
            #* selecting particular TSO option
            select_tso_option = driver.find_element_by_xpath(f"({tso_dropdown_option_xpath})[{i}]")
            tso_name = select_tso_option.get_attribute("innerHTML")     #will be used for naming the file
            select_tso_option.click()
            scrap_logger.info(f"TSO option {tso_name} selected")
            time.sleep(1)
            
            #* clicking DataType dropdown for the respective TSO option
            data_type_dropdown = driver.find_element_by_name("dataType")
            data_type_dropdown.click()
            scrap_logger.info("DataType dropdown clicked")
            time.sleep(1)
            
            #* finding total available DataType options for the selected TSO
            data_type_options_xpath = "//div[contains(@class,'input-group input-group-sm')]/select[contains(@name,'dataType')]/option"
            data_type_options = driver.find_elements_by_xpath(data_type_options_xpath)
            scrap_logger.info(f"Total DataType options for {tso_name} = {len(data_type_options)}")
            
            
            #* going through each and every available DataType options one by one
            scrap_logger.info("going through each and every available DataType options one by one")
            for j in range(1, len(data_type_options) + 1):
                
                #* selecting particular DataType option
                select_datatype_option = driver.find_element_by_xpath(f"({data_type_options_xpath})[{j}]")
                datatype_name = select_datatype_option.get_attribute("innerHTML")       ##will be used for naming the file
                select_datatype_option.click()
                scrap_logger.info(f"DataType option {datatype_name} selected")
                
                #* submitting the selections
                submit = driver.find_element_by_id("submit-button")
                scrap_logger.info("submitting the selections")
                submit.click()
                
                #* finding the table output
                table = driver.find_element_by_xpath("//table[contains(@id,'data-table')]").get_attribute('outerHTML')
                df = pd.read_html(table)
                if len(df) != 0:
                    df = df[0]
                    file_name = f"{tso_name}_{datatype_name}.csv"
                    df.to_csv(os.path.join(download_folder,file_name))
                    scrap_logger.info(f"{file_count} - {file_name} file downloaded")
                    file_count += 1
        
        driver.close()
        driver.quit()
        
        return True
    
    except Exception:
        scrap_logger.exception("Exception occured while downloading files")
        if driver:
            driver.close()
            driver.quit()
        return False



def merge_files(download_path, output_filepath):
    
    """
    [merge_files]
        - it will collect all the data from downloaded CSV files one by one
        - then it will concatenate the collected data into resultant dataframe
        - this resultant dataframe will be converted to OUTPUT CSV file
    """
    
    try:
        resultant_df =  pd.DataFrame(columns = [
            "Date",
            "Time from",
            "Time to",
            "betr. import [MW]",
            "betr. export [MW]",
            "qual. import [MW]",
            "qual. export [MW]"
        ])
        merge_logger.info("File merging started")
        extension = 'csv'
        os.chdir(download_path)
        total_csv_files = glob.glob('*.{}'.format(extension))
        for csv_file in total_csv_files:
            df = pd.read_csv(csv_file, encoding='UTF-8')
            resultant_df = pd.concat([resultant_df, df], ignore_index=True)
        
        output_file = os.path.join(output_filepath,"Output.csv")
        merge_logger.info(f"output file - {output_file}")
        resultant_df.to_csv(output_file)
        merge_logger.info("File merging completed")
        return True
    
    except Exception:
        merge_logger.exception("Error occured")
        return False