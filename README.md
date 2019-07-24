
# [vahan.parivahan.gov.in](https://vahan.parivahan.gov.in/)

## Introduction

This is a scraping script made in order to scrape the data from the vehicle registration dashboard.


## Ground Rules

-   You need to download  python from the below link
>[python v3.6.9](https://www.python.org/downloads/)
    
-   You need to download the 
>[chrome driver](http://chromedriver.chromium.org/downloads)
    
-   You need to  **clone or download** the below repository
>[https://github.com/abhishekzgithub/vahan_parivahan_scrape](https://github.com/abhishekzgithub/vahan_parivahan_scrape)
- You need to download [Visual Studio code](https://code.visualstudio.com/download)
    
--------------
 ## Getting started
 1. Clone or download the repository or code from the github repository.
 2. Make sure you can open it inside visual studio code.
 3. Goto the **vahan_parivahan_scrape** folder
 >cd **vahan_parivahan_scrape**
 4. Run on the command line
 > pip install pipenv
 > pipenv shell
 > pipenv install
 5. After the above operations has been working fine, run the below command to start scraping the data from the **start** which is after **-f** and **end date** which is after **-t**
 > python scrape_vahan.py -f 2009-12-01 -t 2010-02-01
 6. The results will be downloaded in the same folder where the code is in an excel format.
 
 ## Thanks
 Please give star if you are using or like it.