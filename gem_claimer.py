# gem_claimer.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import sched
import logging
import argparse
import sys


def claim_gems():
    """ 
    Claims 250 free Gems on 'dragonica-extended.com' every 30 min.
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

        # Login to website
        driver.find_element_by_name('user_name').send_keys(USERNAME)
        driver.find_element_by_name('password').send_keys(PASSWORD)
        driver.find_element_by_name('login').click()

        # Navigate to page where claim button is
        try:
            # Not being able to find this element means that the user is not
            # logged in
            driver.find_element_by_id('navi-menu-button-2').click()
        except:
            print('Wrong username or password')
            sys.exit()
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

    # Handle command line arguments
    parser = argparse.ArgumentParser(description='Automatic Gem claimer.')
    parser.add_argument('username', metavar='username',
                            help='Username for dragonica-extended.com')
    parser.add_argument('password', metavar='password',
                            help='Password for dragonica-extended.com')
    parser.add_argument('balance', metavar='gems',
                            help='Current amount of Gems')
    args = parser.parse_args() 

    # Set balance, username and password from command line arguments 
    balance = args.balance 
    USERNAME = args.username
    PASSWORD = args.password

    # Initial call to claim_gems()
    claim_gems()

    # Run scheduler
    scheduler.run()
