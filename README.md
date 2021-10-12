# regelleistung-data-scrapping


<p>
This data scrapping script is developed based on the requirement provided in task.docx
</p>

<ul>
<li>
The python script will trigger the selenium webdriver to perform Webcrawling on the <a>https://www.regelleistung.net/ext/data/?lang=en</a> site. 
</li>
<li>It will look for all the available TSO from the dropdown.
</li>
<li>Then will look for all the available dataTypes for each and every TSO</li>
<li>After selecting the TSO and dataTypes, it will click the submit button</li>
<li>Once the required data is displayed in the form of a table, it will scrap the data present in the data and convert it into respective CSV files</li>
<li> Here, the direct DOWNLOAD OPTION PROVIDED IN THE UI is NOT USED, since files downloaded using that option does not display the data properly and it will cause error during the file merge</li>
</ul>
<br>
<hr>
<br>
<h2>Installation and Setup</h2>
1. To copy the files from repository -

    
    $ git clone https://github.com/NishanthMuruganantham/regelleistung-data-scrapping.git
    

2.To install dependencies, run -

    
    $ pip install -r requirements.txt
    
3.Start the api server - 
    
    $ python main.py

<br>
<hr>
<br>
<h2>Note:</h2>
<ol>
<li>Here the Chromedriver used is version 93.</li>
<li><i>selenium.common.exceptions.WebDriverException: Message: unknown error: cannot find Chrome binary</i> -- if this error occured, please <b>uncomment the 40th line in utils.py </b> and <b> add your chrome path in 14th line in utils.py</b></li>
<li>Here, the direct DOWNLOAD OPTION PROVIDED IN THE UI is NOT USED, since files downloaded using that option does not display the data properly and it will cause error during the file merge</li>
<li> It will take some time to download all the files. Please monitor the progress in the Logfile.log</li>
</ul>