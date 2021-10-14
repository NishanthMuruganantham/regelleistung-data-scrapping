from lxml import html
import pandas as pd
import requests
import datetime
import logging
import glob
import os


base_url = "https://www.regelleistung.net/ext/data/?lang=en"
search_endpoint = "https://www.regelleistung.net/ext/data/?from={}&_download=off&tsoId={}&dataType={}&lang=en"
download_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)),"downloaded_files")
output_filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)),"output_folder")


#* capturing the log information in a log file:-
log_file = os.path.join(os.path.dirname(__file__), "LogFile.log")
logging.basicConfig(filename = log_file,format='%(asctime)s : %(name)8s : %(levelname)s : %(message)s',filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)



#* FINDING AVAILABLE TSO AND DATATYPES
def find_available_tso_and_datatype(page_content,xpath):
    
    """[find_available_tso_and_datatype]
        - this is to fiund the number of options availablr for TSO and DATATYPES
        - It parse the HTML content of the page using LXML 
    Args:
        page_content ([string]): [description]
        xpath ([string]): [description]
    
    Returns:
        [list]: [list containing the number of options available for TSO and DATATYPES]
    """
    
    list1 = []
    list_of_options = page_content.xpath(xpath)
    
    for option in list_of_options:
        list1.append(option.get("value"))
        
    return list1



#* EXTRACTING TABLE DATA USING EQUESTS
def find_table_data(date,tso,data_type):
    """[find_table_data]
        - rfinding the table data by doing a POST request in search URL with date, tso, data_type
    Args:
        date ([datestring]): date before 24 hours (from date)
        tso ([type]): tso option ID
        data_type ([type]): Datatype name
        
    Returns:
        [dataframe]: dataframe of the table present
    """
    page = requests.post(search_endpoint.format(date,tso,data_type))
    page_content = page.text #html.fromstring(page.content)
    page_content = page_content.replace("<div>","")     #* cleaning the data
    page_content = page_content.replace("</div>","")    
    try:
        df = pd.read_html(page_content)
        return df
    except ValueError:
        return False


#* main function to scrap the data
def scrap_data(base_url, download_folder):
    
    """
    [scrap_data]
        - first it will find the available TSO and DATATYPES options in the page using xpath with LXML and Requests
        - then it will do a POST request for the available TSO and DATATYPES options
        - once responded, PANDAS will scrap the table data present in the RESPONSE TEXT
    """
    
    try:
        
        #* removing older files
        for f in os.listdir(download_folder):
            os.remove(os.path.join(download_folder, f))
        
        print("file downloading started. It will take some time to download all the files. Please monitor the progress in LogFile.log")
        
        #* finding yesterday date
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        yesterday = yesterday.strftime("%d.%m.%Y")
        logger.info(f"Date : {yesterday}")
        
        tso_xpath = "//select[contains(@name,'tsoId')]/option"
        datatype_xpath = "//select[contains(@name,'dataType')]/option"
        
        #* finding initial page content with GET request
        page = requests.get(base_url)
        page_content = html.fromstring(page.content)
        
        #* finding the available TSO and DATATYPES options
        available_tso = find_available_tso_and_datatype(page_content, tso_xpath)
        available_datatypes = find_available_tso_and_datatype(page_content, datatype_xpath)
        
        logger.info(f"Available TSO list = {available_tso}")
        logger.info(f"Available datatypes list = {available_datatypes}")
    
        
        file_count = 1
        #* going through each and every available TSO options one by one
        for tso in available_tso:
            
            #* going through each and every available DataType options one by one
            for datatype in available_datatypes:
                
                logger.info(f"trying to find the data for {tso} TSO and {datatype} dataType")
                
                #* finding the table data
                table_data = find_table_data(date = yesterday,tso = tso,data_type = datatype)
                
                if table_data:
                    if len(table_data) != 0:
                        #* writing the found table data in CSV file
                        table_data = table_data[0]
                        file_name = f"{tso}_{datatype}.csv"
                        table_data.to_csv(os.path.join(download_folder,file_name))
                        logger.info(f"{file_count} - {file_name} file downloaded")
                        file_count += 1
        
        return True
    
    except Exception:
        logger.exception("error occured in extracting the data")
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
        logger.info("File merging started")
        extension = 'csv'
        os.chdir(download_path)
        total_csv_files = glob.glob('*.{}'.format(extension))
        for csv_file in total_csv_files:
            df = pd.read_csv(csv_file, encoding='UTF-8')
            resultant_df = pd.concat([resultant_df, df], ignore_index=True)
        
        output_file = os.path.join(output_filepath,"Output.csv")
        logger.info(f"output file - {output_file}")
        resultant_df.to_csv(output_file)
        logger.info("File merging completed")
        return True
    
    except Exception:
        logger.exception("Error occured")
        return False


if __name__ == '__main__':
    file_download = scrap_data(base_url, download_folder)
    
    if file_download:
        print("Files are downloaded. Now trying to merge")
        file_merge = merge_files(download_folder, output_filepath)
        if file_merge:
            print("Files are merged successfully. Please find the Output file in the output folder")
        else:
            print("unable to merge files")
    else:
        print("unable to download the files")