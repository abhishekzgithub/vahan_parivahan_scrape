"""
This file is for helper functions which are need for the exectuion
"""
P_URL="https://vahan.parivahan.gov.in/vahan4dashboard/"
SHORT_TIMEOUT = 5   # give enough time for the loading element to appear
LONG_TIMEOUT = 30  # give enough time for loading to finish
LOADING_ELEMENT_XPATH = '//*[@id="j_idt44_modal"]'
FROM_DATE="//input[@id='id_fromDate_input']"
UPTO_DATE="//input[@id='id_uptoDate_input']"

LOG_FORMAT = "[%(asctime)s]-{%(pathname)s:%(lineno)d}-{%(levelname)s}-{In file ->%(module)s " \
             "In function ->%(funcName)s}-{%(message)s}"
