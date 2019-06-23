from calendar import monthrange
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta, date
import pandas as pd
import argparse
import time,os
import pdb
from traceback import format_exc
from selenium.common.exceptions import NoSuchElementException
import logging
LOG_FORMAT = "[%(asctime)s]-{%(pathname)s:%(lineno)d}-{%(levelname)s}-{In file ->%(module)s " \
             "In function ->%(funcName)s}-{%(message)s}"
logging.basicConfig(filename='output.log',level=logging.INFO,format=LOG_FORMAT)
DRIVER_PATH=r'C:\\Users\\abhis11x\\Music\\bookmarks\\program\\chromedriver_win32\\chromedriver.exe'
#os.path.join(os.getcwd(),'chromedriver_win32','chromedriver.exe')
SHORT_TIMEOUT = 5   # give enough time for the loading element to appear
LONG_TIMEOUT = 30  # give enough time for loading to finish
LOADING_ELEMENT_XPATH = '//*[@id="j_idt44_modal"]'
FROM_DATE="//input[@id='id_fromDate_input']"
UPTO_DATE="//input[@id='id_uptoDate_input']"

all_regions = ['Total', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Chandigarh', 'Daman & Diu', 'Delhi', 'Dadra & Nagar Haveli', 'Goa', 'Gujarat', 'Himachal Pradesh', 'Haryana', 'Jharkhand', 'Jammu & Kashmir','Karnataka', 'Kerala', 'Maharashtra', 'Meghalaya', 'Manipur', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Puducherry', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Tripura', 'Uttrakhand', 'Uttar Pradesh', 'West Bengal']
#python scrape_vahan.py -f 2009-01-01 -t 2009-02-01
start_region=1
end_region=len(all_regions)-1
P_URL="https://vahan.parivahan.gov.in/vahan4dashboard/"
driver=None

def init_webdriver():
    global driver
    # --- Options to make scraping faster
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path = DRIVER_PATH, chrome_options=chrome_options)
    return driver

def wait_for_loading(driver):
    try:
        # wait for loading element to appear
        WebDriverWait(driver, SHORT_TIMEOUT
            ).until(EC.presence_of_element_located((By.XPATH, LOADING_ELEMENT_XPATH)))
        # then wait for the element to disappear
        WebDriverWait(driver, LONG_TIMEOUT
            ).until_not(EC.presence_of_element_located((By.XPATH, LOADING_ELEMENT_XPATH)))
    except TimeoutException:
        print(TimeoutException)
        pass

def get_date_range():
    parser = argparse.ArgumentParser()
    # parser.add_argument('date', type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(), help="from date")
    parser.add_argument('-f', "--from_date",
        help="The Start Date - format YYYY-MM-DD",
        required=True,
        #type=date.fromisoformat #todo
        )
    parser.add_argument('-t', "--to_date",
        help="The End Date format YYYY-MM-DD (Inclusive)",
        required=True,
        #type=date.fromisoformat #todo
        )
    args = parser.parse_args()
    print (args.from_date)
    print (args.to_date)
    start_date = args.from_date
    end_date = args.to_date
    return (start_date,end_date)

def set_date(date_range_xpath,date_range):
    try:
        # get the "from date"
        driver.find_element_by_xpath(date_range_xpath).click()
        time.sleep(0.3)
        # Select Year ui-datepicker-year
        driver.find_element_by_xpath(
            "//select[@class='ui-datepicker-year']/option[text()='" + date_range.strftime('%Y') + "']").click()
        # Select the month
        driver.find_element_by_xpath(
            "//select[@class='ui-datepicker-month']/option[text()='" + date_range.strftime('%b') + "']").click()
        # Select Year ui-datepicker-year
        driver.find_element_by_xpath(
            "//a[@class='ui-state-default' and text()='" + str(int(date_range.strftime('%d'))) + "']").click()
    except Exception as e:
            print(e,' exception in set_from_date')
            pass
    finally:
        print(date_range_xpath,date_range,"has been processed")
def get_first_page(array,start_month,last_day,region,office_text):
    s_no = ""
    type_of_vehicle = ""
    num_sold = ""
    table_id = driver.find_elements_by_xpath(
        "//div[@class='ui-datatable-tablewrapper']/table")
    # get all of the rows in the table
    rows = table_id[0].find_elements(By.TAG_NAME, "tr")
    for row in rows:
        # Get the columns (all the column 2)
        # note: index start from 0, 1 is col 2
        try:
            count = 1
            cols = row.find_elements(By.TAG_NAME, "td")
            for col in cols:
                if count == 1:
                    s_no = col.text
                elif count == 2:
                    type_of_vehicle = col.text
                elif count == 3:
                    num_sold = col.text
                else:
                    count = 0
                count = count + 1
            if not (s_no == "" and type_of_vehicle == "" and num_sold == "") or region == "":
                array.append([str(start_month), str(last_day), region, type_of_vehicle,
                    num_sold, office_text])
                print("Array now has",array)
        except Exception as e:
            print(Exception,format_exc())
            pass
    return array
def save_pagination_data(array,start_month,last_day,region,office_text):
    try:
        # -- GO TO FIRST PAGE
        elem_pno = driver.find_elements_by_class_name("ui-paginator-pages")#pagination
        print("Number of pages",len(elem_pno)+1)
        driver.find_elements_by_class_name("ui-icon-seek-first")[0].click() #seek first page
        time.sleep(0.5)
        #array creating start
        array=get_first_page(array,start_month,last_day,region,office_text)
        #elem_pno = driver.find_elements_by_class_name("ui-paginator-page")
        for page_num in range(1, len(elem_pno)+1):#from page 1 and onwards
            driver.find_elements_by_class_name("ui-icon-seek-next")[0].click()
            wait_for_loading(driver)
            array=get_first_page(array,start_month,last_day,region,office_text)
        # ui-icon-closethick
        driver.find_elements_by_class_name("ui-icon-closethick")[1].click() #close item
        wait_for_loading(driver)
    except IndexError:
        logging.info(format_exc())
        array=get_first_page(array,start_month,last_day,region,office_text)
        # ui-icon-closethick
        driver.find_elements_by_class_name("ui-icon-closethick")[1].click() #close item
        wait_for_loading(driver)
    except Exception:
        print(Exception,format_exc())
        logging.info(format_exc())
    finally:
        print("Final array is \n",array)
    return array
            
def get_offices(array,start_month,last_day,region):
    offices_btn = driver.find_elements_by_class_name("ui-selectonemenu-trigger")
    offices_btn[2].click() #click on office #todo
    time.sleep(0.5)
    no_offices = len(driver.find_elements_by_xpath('//ul[@id="selectedRto_items"]/li')) #get all office
    print("No of offices : ", no_offices+1)
    start_office=1
    #end_office=0
    for j in range(start_office, no_offices + 1):#loop till all the offices
        opened = False
        while opened == False:
            try:
                office = driver.find_element_by_xpath('//ul[@id="selectedRto_items"]/li[{}]'.format(j))#office list
                office_text = office.text #get the name
                if office_text !="":
                    office.click() #click on the office name
                    opened = True #set the status to true
                else:
                    driver.find_elements_by_class_name("ui-selectonemenu-trigger")[2].click()
                wait_for_loading(driver)
            except NoSuchElementException:
                j+=1
            except Exception as e:
                print("*** In exception NOT OPENED office or office not found which is unexpected")
                print(format_exc())
                offices_btn = driver.find_elements_by_class_name("ui-selectonemenu-trigger")
                offices_btn[2].click() #click on office #todo
        print(" *** In office : ", office_text)
        #wait_for_loading(driver)
        # j_idt54
        driver.find_element_by_xpath("//a[@id='j_idt54']").click() #click on vehicle registration "more info"
        wait_for_loading(driver)
        # Click on CHANGE CATEGORY wise table (CLASS)
        driver.find_elements_by_class_name("ui-selectonemenu-trigger")[3].click() #dropdown
        driver.find_element_by_xpath("//li[@id='datatable_rtoWise:dropdown2_2']").click()#"Class Wise"
        wait_for_loading(driver)
        # Run through pages
        array=save_pagination_data(array,start_month,last_day,region,office_text)
    return array

def main():
    try:
        (start_date,end_date)=get_date_range()
        start_date=datetime.strptime(start_date,"%Y-%m-%d")
        end_date=datetime.strptime(end_date,"%Y-%m-%d")
        start_day_month = date(year=start_date.year, month=start_date.month, day=1) #todo
        end_month = date(year=end_date.year, month=end_date.month, day=1) #todo
        # start_day_month=date(year=2019,month=1,day=1) #remove after use
        # end_month=date(year=2019,month=3,day=1) #remove after use
        driver = init_webdriver()
        array = [] # Array to store data to CSV
        while(start_day_month <= end_month):
            last_day_month = date(year=start_day_month.year, month=start_day_month.month, day=(monthrange(start_day_month.year, start_day_month.month)[1]))
            driver.get(P_URL)
            # Change `Type` to "Actual Value"
            driver.find_elements_by_class_name("ui-selectonemenu-trigger")[0].click()
            # Click on "Actual Value"
            driver.find_elements_by_id("j_idt25_3")[0].click()
            wait_for_loading(driver)
            set_date(FROM_DATE,start_day_month)
            print("set_date1 done")
            wait_for_loading(driver)
            set_date(UPTO_DATE,last_day_month)
            print("set_date2 done")
            wait_for_loading(driver)
            # check if j_idt44_modal exists on the page. this is the loading gif
            # Run through the STATES
            for region in range(start_region, (end_region)+1):
                xpath1="//div[@id='j_idt35']//span[@class='ui-icon ui-icon-triangle-1-s ui-c']"#dropdown on the state
                driver.find_element_by_xpath(xpath1).click()
                elem = driver.find_elements_by_id("j_idt35_" + str(region))#state index
                time.sleep(0.2)
                region_name = elem[0].text #state name
                elem[0].click() #CLICK on the state
                time.sleep(0.5)
                wait_for_loading(driver)
                # --- GET OFFICES
                array=get_offices(array,start_day_month,last_day_month,region_name)
                logging.info("normal output is \n ",array)
                df = pd.DataFrame(array, columns = ['begining_date', 'end_date', 'region', 'type_of_vehicle','num_sold', 'office'])
                df.to_csv(f'{region_name}_{start_day_month}_{last_day_month}.csv', index=None)
            if start_day_month.month == 12:
                start_day_month = date(year=start_day_month.year+1, month=1, day=1)
            else:
                start_day_month = date(year=start_day_month.year, month=start_day_month.month+1, day=1)
    except:
        logging.info(format_exc())
        logging.info("except output is \n",array)
        df = pd.DataFrame(array, columns = ['begining_date', 'end_date', 'region', 'type_of_vehicle','num_sold', 'office'])
        df.to_csv(f'{region_name}_{start_day_month}_{last_day_month}_except.csv', index=None)
    finally:
        logging.info("----------------------------------done------------------------------")

if __name__=='__main__':
    main()