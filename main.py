from utils import download_csv_files, merge_files
import logging
import os


base_url = "https://www.regelleistung.net/ext/data/?lang=en"
chrome_driver = os.path.join(os.path.abspath(os.path.dirname(__file__)),"chromedriver.exe")
download_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)),"downloaded_files")
output_filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)),"output_folder")


#* capturing the log information in a log file:-
log_file = os.path.join(os.path.dirname(__file__), "LogFile.log")
logging.basicConfig(filename = log_file,format='%(asctime)s : %(name)8s : %(levelname)s : %(message)s',filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    file_download = download_csv_files(base_url, chrome_driver, download_folder)
    
    if file_download:
        print("Files are downloaded. Now trying to merge")
        file_merge = merge_files(download_folder, output_filepath)
        if file_merge:
            print("Files are merged successfully. Please find the Output file in the output folder")
        else:
            print("unable to merge files")
    else:
        print("unable to download the files")
