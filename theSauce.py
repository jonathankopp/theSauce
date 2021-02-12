import os
import sys
import six
import pause
import argparse
from selenium import webdriver
from dateutil import parser as date_parser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


BETHPAGE_GOLF_HOME = "https://foreupsoftware.com/index.php/booking/19765/2431#teetimes"
facility           = ""
timePath           = "//*[@id='times']/li[5]/div"



def run(driver, username, password, login_time=None, release_time=None,
        page_load_timeout=None, course = "Bethpage Black Course",amt_ppl=2):
    driver.maximize_window()
    driver.set_page_load_timeout(page_load_timeout)

    try:
        login(driver=driver, username=username, password=password)
    except Exception as e:
        print("Failed to login: " + str(e))
        six.reraise(Exception, e, sys.exc_info()[2])

    if release_time:
        print("Waiting until release time: " + release_time)
        pause.until(date_parser.parse(release_time))
        print("Waiting for reserve a time now button to become clickable")
        wait_until_visible(driver=driver, xpath="//*[@id='profile-main']/div/ul/li/a")

        print("Clicking reserve a time button")
        driver.find_element_by_xpath("//*[@id='profile-main']/div/ul/li/a").click()


    wait_until_visible(driver=driver, xpath="//*[@id='schedule_select']")
    print("Successfully completed first steps")
    
    

    select_facility(driver = driver, course = course, amt=amt_ppl)
    # select_time(driver=driver)
    return


def login(driver, username, password):
    try:
        print("Requesting page: " + BETHPAGE_GOLF_HOME)
        driver.get(BETHPAGE_GOLF_HOME)
    except TimeoutException:
        print("Page load timed out but continuing anyway")

    print("Waiting for Resident button to become clickable")
    wait_until_clickable(driver=driver, xpath="//*[@id='content']/div/button[1]")

    print("Clicking Resident button")
    driver.find_element_by_xpath("//*[@id='content']/div/button[1]").click()

    print("Waiting for Login button to become clickable")
    wait_until_clickable(driver=driver, xpath="//*[@id='teetime-login']/div/p[1]/button")

    print("Clicking Login button")
    driver.find_element_by_xpath("//*[@id='teetime-login']/div/p[1]/button").click()

    print("Waiting for login fields to become visible")
    wait_until_visible(driver=driver, xpath="//*[@id='login_email']")

    print("Entering username and password")
    email_input = driver.find_element_by_xpath("//*[@id='login_email']")
    email_input.clear()
    email_input.send_keys(username)
    password_input = driver.find_element_by_xpath("//*[@id='login_password']")
    password_input.clear()
    password_input.send_keys(password)

    print("Logging in")
    driver.find_element_by_xpath("//*[@id='login']/div/div[3]/div/button[1]").click()



# dropdown for facility
def select_facility(driver, course, amt):
    facilities = ['Bethpage Black Course','Bethpage 9 Holes Midday Blue or Yellow Course',
    'Bethpage Blue Course','Bethpage Early AM 9 Holes Blue','Bethpage Early AM 9 Holes Yellow',
    'Bethpage Green Course','Bethpage Red Course','Bethpage Yellow Course']
    print("Clicking schedule select button")
    driver.find_element_by_xpath("//*[@id='schedule_select']").click()

    print("Waiting for dropdown element to be clickable")
    wait_until_visible(driver=driver, xpath="//*[@id='schedule_select']/option["+str((facilities.index(course)+1))+"]")

    print("Clicking facility")
    driver.find_element_by_xpath("//*[@id='schedule_select']/option["+str((facilities.index(course)+1))+"]").click()

#   dONT NEED IF BLACK COURSE
    print("waiting for resident thang")
    wait_until_visible(driver=driver, xpath="//*[@id='content']/div/button[1]")

    print("clicking resident thing")
    driver.find_element_by_xpath("//*[@id='content']/div/button[1]").click()

    print("waiting for person amount")
    wait_until_visible(driver=driver, xpath="//*[@id='nav']/div/div[3]/div/div/a[4]")

    print("clicking person amount")
    driver.find_element_by_xpath("//*[@id='nav']/div/div[3]/div/div/a[4]").click()

    # //*[@id="date"]/div/div[1]/table/tbody/tr[3]/td[2]
    print("waiting for day")
    wait_until_visible(driver=driver, xpath="//*[@id='date']/div/div[1]/table/tbody/tr[2]/td[1]")

    print("clicking day")
    driver.find_element_by_xpath("//*[@id='date']/div/div[1]/table/tbody/tr[2]/td[1]").click()
    print("Done Selecting Facitlity and amount of people")

# def select_time(driver):
#     print("Waiting for dropdown element to be clickable")
#     wait_until_visible(driver=driver, xpath="//*[@id='times']/li[5]")

#     print("Clicking facility")
#     driver.find_element_by_xpath("//*[@id='times']/li[5]").click()


def wait_until_clickable(driver, xpath=None, class_name=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))


def wait_until_visible(driver, xpath=None, class_name=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--username", required=True)
    # parser.add_argument("--password", required=True)
    parser.add_argument("--release-time", type=str, default='19:01')
    parser.add_argument("--page-load-timeout", type=int, default=2)
    args = parser.parse_args()

    executable_path = os.getcwd()+"/chromedriver.exe"
    driver          = webdriver.Chrome(ChromeDriverManager().install())
    driver          = webdriver.Chrome(executable_path=executable_path, chrome_options=webdriver.ChromeOptions())


    ########################Spencer, here is where you input what you want##########################
    course           = "Bethpage Red Course"          # you can put any course name here
    amount_of_people = 4                                # you can put any amnt here
    username         = "username@gmail.com"        # you can put your username (email) here
    password         = "password"                   # you can put your password here
    ################################################################################################



    run(driver=driver, username=username, password=password, release_time=args.release_time, 
        page_load_timeout=args.page_load_timeout,course=course,amt_ppl=amount_of_people)