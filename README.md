# regelleistung-data-scrapping


<p>
This data scrapping script is developed based on the requirement provided in task.docx
</p>

<ul>
<li>
This script is based on DATA SCRAPPING USING PYTHON REQUEST LIBRARY
</li>
<li>
First it will do a GET request on <a>https://www.regelleistung.net/ext/data/?lang=en</a> to find the available TSO and Datatype options. 
</li>
<li>Then it will do a POST request on <a>https://www.regelleistung.net/ext/data/?from={DATE}&_download=off&tsoId={TSO_ID}&dataType={DATATYPE}&lang=en</a>  to find the data available for the specified TSO and Datatype
</li>
<li>Then it will convert the fetched table data into a DSataframe using Pandas</li>
<li>Once all the data are extarcted, it will perform Merge on all downloaded CSV files and convert that into a single CSV file</li>
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
    
    $ python scrapping_with_requests.py

<br>
<hr>
<br>
<h2>Note:</h2>
<ol>

<li> It will take some time to download all the files. Please monitor the progress in the Logfile.log</li>
</ul>
