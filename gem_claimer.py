# gem_claimer.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime
import time
import sched
import argparse
import sys


def claim_gems():
    """ 
    Claims 250 free Gems on 'dragonica-extended.com' every 30 min.
    """ 

    # Set options for webdriver
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless') # Does not open browser
    options.add_argument('--mute-audio') # Suppose to mute audio

    # Initialize driver  
    driver = webdriver.Firefox(executable_path='./geckodriver', 
                            firefox_options=options)

    # Wait for expected condition for 30 sec, otherwise raise exception 
    wait = WebDriverWait(driver, 30)

    # Load starting page
    driver.get('http://dragonica-extended.com')

    # Login to website
    driver.find_element_by_name('user_name').send_keys(USERNAME)
    driver.find_element_by_name('password').send_keys(PASSWORD)
    driver.find_element_by_name('login').click()

    # Navigate to the page with claim button. If these elements cannot be
    # found then it means that the user is not logged in.
    try:
        driver.find_element_by_id('navi-menu-button-2').click()
        driver.switch_to_frame('ifrm')
    except:
        print('Incorrect username or password')
        driver.quit()
        sys.exit()

    # Save old balance to notice changes after claiming
    old_balance = (wait.until(
            EC.presence_of_element_located((By.ID, 'CashDP'))
        )).text

    # Claim Gems
    (wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'btn_claim'))
        )).click()
    
    # Wait until the amount of Gems changes. If they dont change then that
    # probably means that it was less than 30 min before last claim. It will
    # then try to claim again in 5 min. Otherwise claim again in 30 min.
    try:
        wait.until_not(EC.text_to_be_present_in_element(
                (By.ID, 'CashDP'), old_balance))
    except:
        time = str(datetime.now())[:-7]
        print('[{}]: Balance unchanged. Trying again in 5 min...'.format(\
                                                                    time))
        scheduler.enter(300, 1, claim_gems)
    else:
        time = str(datetime.now())[:-7]
        new_balance = driver.find_element_by_id('CashDP').text
        print('[{}]: New balance: {}'.format(time, new_balance))
        scheduler.enter(1800, 1, claim_gems)
    finally:
        driver.quit()


def handle_command_line_arguments():
    parser = argparse.ArgumentParser(description='Automatic Gem claimer.')

    parser.add_argument('username', metavar='username',
                            help='Username for dragonica-extended.com')

    parser.add_argument('password', metavar='password',
                            help='Password for dragonica-extended.com')

    args = parser.parse_args() 

    return args

if __name__ == '__main__':

    # Initialize scheduler 
    scheduler = sched.scheduler(time.time, time.sleep)

    # Handle command line arguments
    args = handle_command_line_arguments()

    USERNAME = args.username
    PASSWORD = args.password

    # Initial call to claim_gems()
    claim_gems()

    # Run scheduler
    scheduler.run()
