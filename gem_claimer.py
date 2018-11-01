# gem_claimer.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from datetime import datetime
import time
import sched
import sys
import getpass
import os


def claim_gems():
    """ 
    Claims 250 free Gems on 'dragonica-extended.com' every 30 min.
    """ 
    
    try:

        # Set options for webdriver
        options = webdriver.FirefoxOptions()
        #options.add_argument('--headless') # Does not open browser
        options.add_argument('--mute-audio') # Suppose to mute audio

        # Initialize driver  
        driver = webdriver.Firefox(executable_path='./geckodriver', 
                                firefox_options=options)

        # Load starting page
        driver.get('http://dragonica-extended.com')

        # Login to website
        driver.find_element_by_name('user_name').send_keys(USERNAME)
        driver.find_element_by_name('password').send_keys(PASSWORD)
        driver.find_element_by_name('login').click()

        # Wait for expected condition for 60 sec, otherwise raise exception 
        wait = WebDriverWait(driver, 60)

        # Navigate to the page with claim button. If these elements cannot be
        # found then it means that the user is not logged in.
        try:
            (wait.until(EC.presence_of_element_located(
                        (By.ID, 'navi-menu-button-2')))).click()
            driver.switch_to_frame('ifrm')
        except:
            print('Incorrect username or password')
            driver.quit()
            sys.exit()

        # Claim Gems
        (wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'btn_claim')))).click()
       
    # If browser timesout just try again in 5 minutes
    except TimeoutException:
        time = str(datetime.now())[:-7]
        print('[{}] Browser timeout. Trying again in 5 min...'.format(time))
        scheduler.enter(300, 1, claim_gems)

    # Exit on keyboard interrupt
    except KeyboardInterrupt:
        print()
        sys.exit()

    # If some other exception occured raise it 
    except Exception as e:
        raise e

    # If everything schedule next claim in 30 minutes
    else:
        time = str(datetime.now())[:-7]
        print('[{}] Claimed 250 Gems. Claiming again in 30 min...'.format(\
                                                                    time))
        scheduler.enter(1800, 1, claim_gems)

    # Whatever happens quit driver 
    finally:

        try:
            driver.quit()
        except:
            pass

if __name__ == '__main__':

    # Initialize scheduler 
    scheduler = sched.scheduler(time.time, time.sleep)

    try:
        USERNAME = input('Username: ')
        PASSWORD = getpass.getpass('Password: ')
    except KeyboardInterrupt:
        print()
        sys.exit()

    os.system('cls' if os.name == 'nt' else 'clear') # Windows / Unix

    # Call claim_gem() and run scheduler
    claim_gems()
    scheduler.run()
