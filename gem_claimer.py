# gem_claimer.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import sched
import logging
import argparse


def claim_gems():
    """ 
    Goes to dragonica-extended website, logs in with USERNAME and 
    PASSWORD specified in file 'login.txt' and claims 250 Gems every 30 min.
    """ 

    global balance

    try:
        # Set options for webdriver
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless') # Don't open actual browser
        options.add_argument('--mute-audio') # This doesn't seem to work

        # Initialize driver  
        driver = webdriver.Firefox(executable_path='./geckodriver', 
                            firefox_options=options)

        # Load starting page
        driver.get('http://dragonica-extended.com')

        # Login to the website
        driver.find_element_by_name('user_name').send_keys(USERNAME)
        driver.find_element_by_name('password').send_keys(PASSWORD)
        driver.find_element_by_name('login').click()

        # Navigate to page where claim button is
        driver.find_element_by_id('navi-menu-button-2').click()
        driver.switch_to_frame('ifrm')
       
        # Wait for expected condition for 5 sec, otherwise raise exception 
        wait = WebDriverWait(driver, 5)

        # Claim Gems
        (wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, 'btn_claim'))
            )).click()
        
        # Save the amount of gems after attempted claim 
        try:
            wait.until_not(
                    EC.text_to_be_present_in_element(
                    (By.ID, 'CashDP'), balance))

            balance = driver.find_element_by_id('CashDP').text

        # If balance is unchanged
        except: 
            raise Exception('Balance unchanged')

    # If some error occurred
    except Exception as e:
        # Log
        logging.error(e)

        # Try to claim again in 30 seconds
        scheduler.enter(30, 1, claim_gems)

    # If everything went as it should
    else: 
        # Log
        logging.info('New balance: {}'.format(balance))

        # Claim again in 30 minutes 
        scheduler.enter(1800, 1, claim_gems)

    # Whatever happens
    finally:
        # Quit driver (basically close browser)
        driver.quit()

if __name__ == '__main__':

    # Configure logging
    logging.basicConfig(filename='balance.log', level=logging.INFO,
        format='%(asctime)s:%(levelname)s: %(message)s')

    # Initialize scheduler 
    scheduler = sched.scheduler(time.time, time.sleep)

    # Store username/password from file 'login.txt' in USERNAME/PASSWORD
    with open('login.txt', 'r') as f:
        USERNAME, PASSWORD = f.read().split('\n')[:2]
    
    # Handle arguments
    parser = argparse.ArgumentParser(description='Automatic Gem claimer.')
    parser.add_argument('balance', metavar='Gems',
                            help='Current amount of Gems')
    args = parser.parse_args() 

    # Set intial balance 
    balance = args.balance 

    # Initial call to claim_gems()
    claim_gems()

    # Run scheduler
    scheduler.run()
