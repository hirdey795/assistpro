""" 
NOTE: This file is only for scraping unis/majors/classes, this is only for getting data for the front page
      of the website

"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import json
import time

# Text to speech, just for demo purposes
from tts import speak

class WebBot():
    
    def __init__(self):
        speak("Initializing WebBot...")
        options = Options()
        options.add_experimental_option("detach", True)  # So browser doesn't close prematurely
        options.add_argument("--window-size=1440,960")  # Adjust the width and height as needed
        options.add_argument("--headless")  # Uncomment for headless mode
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.url = "https://assist.org"
        speak("Initialization finished...")
            
    def open_articulation_agreements(self, institution_num, agreement_num):
        driver = self.driver
        actions = ActionChains(driver)
        driver.get(self.url)
        speak("Reading data...")
        
        try:
            # Scroll to make drop down clickable to enter institution
            dropDownInstitution = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='fromInstitution']"))
            )
            actions.move_to_element(dropDownInstitution).click().perform()
            
            # Enter Uni
            institution = driver.find_element(By.XPATH, f"//div[contains(@id, '-{institution_num}') and @class='ng-option' and @role='option']/span[@class='ng-option-label']")
            institution.click()
            
            time.sleep(0.3)  # Slow down to enter inputs properly
            
            # Scroll to make drop down clickable to enter agreements
            dropDownAgreement = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='agreement']"))
            )
            actions.move_to_element(dropDownAgreement).click().perform()
            
            # Select College
            agreement = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[contains(@id, '-{agreement_num}')]"))
            )
            actions.move_to_element(agreement).click().perform()
            
            # Click on agreement
            driver.find_element(By.XPATH, "/html/body/app-root/div[2]/app-home-component/section[@class='content']/app-form-container/div[@class='formArea']/div[@id='agreementInformationForm']/app-transfer-agreements-form/div[@class='panel agreements']/div[@class='panel-content']/form[@id='transfer-agreement-search']/div[@class='d-flex justify-content-center']/button[@class='btn btn-primary']").click()
            
        except Exception as e:
            speak(f"Error on page 1: {e}")
            self.restart_browser()
    
    def scrape_articulations(self, major) -> dict:
        driver = self.driver
        actions = ActionChains(driver)
        try:
            chooseMajor = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[@class='viewByRow'][{major}]"))
            )
            actions.move_to_element(chooseMajor).click().perform()
        except Exception as e:
            print(e)
            driver.quit() 
            return

        # time.sleep(1)
        try:
            uniName = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,  "//div[@class='instReceiving']/p[@class='inst']"))
            ).text
            # uniName = driver.find_element(By.XPATH, "//div[@class='instReceiving']/p[@class='inst']").text
            uniName = uniName.replace("To: ", "")
            majorName = driver.find_element(By.XPATH, "//div[@class='resultsBoxHeader']/h1").text

            uniCoursesElements = driver.find_elements(By.XPATH, "//div[@class='rowReceiving']")

            uniCourses = [element.text.split("\n")[0] for element in uniCoursesElements]

            # Adjusted data structure to match the required format
            data = {
                uniName: {
                    majorName: uniCourses
                }
            }

            return data

        except Exception as e:
            speak(e)
            return None

    def return_to_home(self):
        driver = self.driver
        actions = ActionChains(driver)
        try:
            returnToHome = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div[2]/app-transfer/section[@class='left-panel']/div[@class='logo-lockup']/a[@class='btn btn-primary']"))
                    )
            actions.move_to_element(returnToHome).click().perform()

            click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//form[@id='transfer-agreement-search']//div[@class='d-flex justify-content-center']/button[@class='btn btn-primary']")))
            actions.move_to_element(click).click().perform()

        except Exception as e:
            print(e)
            self.restart_browser()
    
    def restart_browser(self):
        print("Restarting the browser...")
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Error quitting the browser: {e}")
        self.__init__()
        
    def quit(self):
        self.driver.quit()

def write_data_to_file(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        with open(file_path, "r") as file:
            existing_data = json.load(file)
    except:
        existing_data = {}

    # Merging existing data with new data
    for uni, majors in data.items():
        if uni not in existing_data:
            existing_data[uni] = {}
        for major, classes in majors.items():
            if major not in existing_data[uni]:
                existing_data[uni][major] = []
            # Merging classes while avoiding duplicates
            existing_data[uni][major] = list(set(existing_data[uni][major] + classes))

    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=4)
        # speak("Added new data to file")
        print("Added new data to file")

if __name__ == "__main__":
    
    """ 
    NOTE: The first commented block below is for testing, and not meant to be used for automated scraping
    """
    # bot = WebBot()
    # file_name = "client/src/dataset/uni_and_classes_2.json"
    # bot.open_articulation_agreements(136, 106)  # Institution = 136, Agreement = 106
    # data = bot.scrape_articulations(32)  # Major = 32
    # if data:
    #     write_data_to_file(file_name, data)
    # time.sleep(1)
    # bot.quit()
    # speak("Exited chrome driver")
    
    """ 
    NOTE: The commented block below is the script to get all majors and courses from UC & CSUs
    NOTE: Note that we already have scraped all the major courses, can be located at "client\src\dataset\uniMajorsCoursesCopy.json"
    """
    # bot = WebBot()
    # file_name = "client/src/dataset/uni_and_classes_3.json"
    
    # for i in range(10, 26):
    #     bot.open_articulation_agreements(i, 76)
    #     j = 1
    #     while True:
    #         try:
    #             data = bot.scrape_articulations(j)
    #             if data:
    #                 write_data_to_file(file_name, bot.scrape_articulations(j))
    #             else:
    #                 break
    #         except Exception as e:
    #             print(e)
    #             break
    #         j += 1
    #     bot.return_to_home()
    
    # for i in range(136, 144):
    #     bot.open_articulation_agreements(i, 76)
    #     j = 1
    #     while True:
    #         try:
    #             data = bot.scrape_articulations(j)
    #             if data:
    #                 write_data_to_file(file_name, bot.scrape_articulations(j))
    #             else:
    #                 break
    #         except Exception as e:
    #             print(e)
    #             break
    #         j += 1
    #     bot.return_to_home()
        
    # bot.quit()
        
