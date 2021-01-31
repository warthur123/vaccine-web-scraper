import time
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#### helper function that gets number of available appointments
def get_appointments(list_of_properties):
    for item in list_of_properties:
        if "Available Appointments" in item.text:
            return item.text[len(item.text) - 2:len(item.text)]
    return ""

PATH = "assets/chromedriver"
URL = "https://www.marylandvax.org/clinic/search"

while True:

    driver = webdriver.Chrome(PATH)
    has_next_page = True
    #driver.get("/Users/arthurwu/Desktop/vaccine_web_scraper/test.html") #test
    driver.set_window_position(-100000, 0)
    driver.get(URL)     # fetch and open website

    while has_next_page:        # loop through each page of results

        main = driver.find_element_by_class_name("mt-24")
        results = main.find_elements_by_class_name("field-fullwidth")

        for result in results:
            header = result.find_element_by_tag_name("h4")      # get address
            #print(header.text)

            if "Prince George" in header.text:      # if address contains "Prince George"                                
                has_appointments = result.find_elements_by_tag_name("p")

                number_of_appointments = get_appointments(has_appointments)
            
                if int(number_of_appointments) > 0:     # if number of available appointments is more than 0
                    playsound('assets/beep.mov')       # play beep sound
                    #print("Beep: Found match")  

        if driver.find_elements_by_xpath("//span[contains(@class, 'next') and contains(@class, 'disabled')]"):      # if no next page, stop running
            has_next_page = False
            break
    
        driver.find_element_by_xpath("//span[contains(@class, 'next')]/a").click()      # Go to next page by clicking 'next' button
        driver.get(driver.current_url)      # update driver to be next page
    
    driver.quit()

    print("Scraped Successfully.")

    time.sleep(300)