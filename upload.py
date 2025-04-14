# Make boring things interesting :)

# easy to install selenium, just pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
from io import StringIO
import argparse
from selenium.webdriver.edge.options import Options

def generate_csv(txtfile, csvfile): #txt file is not convenient, so transfer to csv first
    line_count = 0
    with open(txtfile, 'r') as f:
        data = f.read()
    print(data)
    data_io = StringIO(data)
    
    df = pd.read_csv(data_io, sep=r'\s+', header=None)
    
    print(df)
    
    df.to_csv(csvfile, index=False, header=False)
    with open(txtfile, 'r') as f:
        line_count = len(f.readlines())

    return line_count

def ini_db(driver, username, password): #initialize the website, typing in your username and pw and clicking the login button
    driver.get("https://mtd-operator-ui.app.cern.ch/assembleSensorModule")
    time.sleep(15)
    
    username_input = driver.find_element(By.XPATH, "//input[@aria-label='Username']")
    username_input.send_keys(username)
    
    password_input = driver.find_element(By.XPATH, "//input[@aria-label='Password']")
    password_input.send_keys(password)
    
    login_button = driver.find_element(By.XPATH, "//p[text()='Login']")
    login_button.click()

    time.sleep(15)

def clear_code(element): # to clear the string typed before
    element.click()
    element.send_keys(Keys.COMMAND, "a")  
    element.send_keys(Keys.BACKSPACE)

def upload_data(driver, csvfile, line):# key function, loop all the info you want to upload, if there is an exception, it will break
    df = pd.read_csv(csvfile)
    logout_button = driver.find_element(By.XPATH, "//p[text()='Logout']")
    for i in range(0, line):
        SM_barcode_str = df.iloc[i, 0]
        left_sipm_str = df.iloc[i, 1]
        LYSOMatrix_str = df.iloc[i, 2]
        right_sipm_str = df.iloc[i, 3]
        name_str = df.iloc[i, 4]
        gambit_str = df.iloc[i, 5]
        date_str = df.iloc[i, 6]
        print(f"SM barcode={SM_barcode_str}, l_sipm={left_sipm_str}, lyso={LYSOMatrix_str}, r_sipm={right_sipm_str}")
        time.sleep(5)
     
        SM_barcode = driver.find_element(By.XPATH, "//input[@aria-label='SensorModule barcode']")
        driver.execute_script("arguments[0].scrollIntoView(true);", logout_button)
        clear_code(SM_barcode)
        SM_barcode.send_keys("{0}".format(SM_barcode_str))
        time.sleep(5)
        
        left_sipm = driver.find_element(By.XPATH, "//input[@aria-label='Left SiPMArray (last five digits)']")
        clear_code(left_sipm)
        left_sipm.send_keys(f"{left_sipm_str}")
        time.sleep(5)

        lyso = driver.find_element(By.XPATH, "//input[@aria-label='LYSOMatrix']")
        clear_code(lyso)
        lyso.send_keys(f'{LYSOMatrix_str}')
        time.sleep(5)

        right_sipm = driver.find_element(By.XPATH, "//input[@aria-label='Right SiPMArray (last five digits)']")
        clear_code(right_sipm)
        right_sipm.send_keys(f'{right_sipm_str}')
        time.sleep(5)

        comment = driver.find_element(By.XPATH, "//textarea[@aria-label='Operator comment']")
        clear_code(comment)
        comment.send_keys(f"{name_str} {gambit_str} {date_str}")
        time.sleep(15)
        
        try:
            glue_button = driver.find_element(By.XPATH, "//p[text()='Glue']")
            ActionChains(driver).move_to_element(glue_button).click().perform()
        except Exception as e:
            print(f"EXCEPTION, {e}")
            print(f"Maybe wrong pair: SM barcode={SM_barcode_str}, l_sipm={left_sipm_str}, lyso={LYSOMatrix_str}, r_sipm={right_sipm_str}")
            break
        time.sleep(20)
        # driver.execute_script("arguments[0].scrollIntoView(true);", glue_button)
        try:
            confirm_button = driver.find_element(By.XPATH, "//p[text()='Confirm']")
            confirm_button.click()
        except Exception as e:
            print(f"EXCEPTION, {e}")
            break

        time.sleep(10)
        # driver.execute_script("window.scrollTo({ top: 0, behavior: 'smooth' });")
        # time.sleep(2)


def main():
    # All you need is txt file name, csv file name, your Username and password. Please copy data from google spread sheet to your txt file.
    # Run like this: python upload.py --txt lyso.txt --csv lyso.csv --user Username --pw password
    parser = argparse.ArgumentParser(description='input parameters to the apply')
    parser.add_argument('--txt', type=str, default='lyso.txt', required=True, help='txt file name')
    parser.add_argument('--csv', type=str, default='lyso.csv', required=True, help='csv file name')
    parser.add_argument('--user', type=str, required=True, help='Username')
    parser.add_argument('--pw', type=str, required=True, help='password')
    args = parser.parse_args()
    
    line_count = 0
    line_count = generate_csv(args.txt, args.csv)
    print(line_count)
    # if you wish, you can change to Chrome, Firefox and etc.  
    # But remmeber to turn your browser to development mode or use Webdriver, so you can handle page automatically
    # !!!headless mode is needed!!! Or it will be disturbed by your other activities in you computer.
    options = Options()
    options.headless = True
    driver = webdriver.Edge(options=options)

    ini_db(driver, args.user, args.pw)

    upload_data(driver, args.csv, line_count-1)

    time.sleep(10)

    print("upload DONE")

if __name__ == "__main__":
    main()
