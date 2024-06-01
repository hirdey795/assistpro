# importing necessary packages 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json
import time

"""
XPath Cheat Sheet = "https://quickref.me/xpath"
Assist.org = "https://assist.org"
Extra websites = " "
"""
class WebBot():
    
    def __init__(self):
        
        print("Initializing WebBot...")
        
        options = Options()
        options.add_experimental_option("detach", True) # So browser don't close prematurely
        options.add_argument("--window-size=1920,1080")  # Adjust the width and height as needed
        self.driver = webdriver.Chrome(options=options)
        self.url = "https://assist.org"
        print("Initialized finished...")
        
    def open_articulation_agreements(self, institution_num, agreement_num):
        
        driver = self.driver
        actions = ActionChains(driver)
        driver.get(self.url)
        print("Reading data...")
        
        """ 
        THIS IS A HACK FOR SCC -> BEKRELEY EECS FOR NOW, 
        CHANGE LATER FOR A LOOP FOR ALL UNIVERSITIES
        """
        
        try:
            
            """ 
            HACK
            Enter Institution for Sacramento City College
            """
            
            # Scroll to make drop down clickable to enter institution
            dropDownInstitution = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='fromInstitution']"))
            )
            actions.move_to_element(dropDownInstitution).click().perform()
            
            # Enter college
            # 113 = Sacramento City College
            institution = driver.find_element(By.XPATH, f"//div[contains(@id, '-{institution_num}') and @class='ng-option' and @role='option']/span[@class='ng-option-label']")
            institution.click()
            
            # Hack: Slow down to enter inputs properly, else it won't work
            time.sleep(0.3)
            
            """ 
            HACK
            Enter Agreement with Berkeley
            """
            
            # Scroll to make drop down clickable to enter agreements
            dropDownAgreement = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='agreement']"))
            )
            actions.move_to_element(dropDownAgreement).click().perform()
            
            # select University
            # 26 = Berkeley
            agreement = driver.find_element(By.XPATH, f"//div[contains(@id, '-{agreement_num}') and @class='ng-option' and @role='option']/span[@class='ng-option-label']")
            agreement.click()
            
            # Click on agreement HACK
            driver.find_element(By.XPATH, "/html/body/app-root/div[2]/app-home-component/section[@class='content']/app-form-container/div[@class='formArea']/div[@id='agreementInformationForm']/app-transfer-agreements-form/div[@class='panel agreements']/div[@class='panel-content']/form[@id='transfer-agreement-search']/div[@class='d-flex justify-content-center']/button[@class='btn btn-primary']").click()
            
        except Exception as e:
            print(f"Error on page 1: {e}")
            self.driver.quit()
            return
        
        
    """ 
    Scraping information for articulation.
    HACK: This is for EECS major for now
    """
    # EECS: //div[@class='viewByRow'][32]
    def scrape_articulations(self, major):
        """ 
        Args:
        major: Int
        """
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
        
        """
        This sentence is to take all of the courses and create a dictionary 
        
        Key: MATH1A, Value: MATH400 ("Sacramento City College"), MATH400 ("American River College")
        e.g.
        
        Agreement = UNI + "<->" + COLLEGE
        
        { 
            "Berkeley <-> Sacramento City College" : { "MATH1A" : "MATH400" }
        }
        """
        time.sleep(1)
        try:
            uniName = driver.find_element(By.XPATH, "//div[@class='instReceiving']/p[@class='inst']").text
            collegeName = driver.find_element(By.XPATH, "//div[@class='instSending']/p[@class='inst']").text
            
            uniCoursesElements = driver.find_elements(By.XPATH, "//div[@class='rowReceiving']")
            collegeCoursesElements = driver.find_elements(By.XPATH, "//div[@class='rowSending']")
            
            uniCourses = [element.text.split("\n")[0] for element in uniCoursesElements]
            collegeCourses = [element.text.split("\n")[0] for element in collegeCoursesElements]
            
            print("----Uni Courses----")
            print(uniCourses)
            print("----")
            
            print("----College Courses---")
            print(collegeCourses)
            print("----")
            
            articulation_dict = {uniCourses:collegeCourses for uniCourses, collegeCourses in zip(uniCourses, collegeCourses)}
            
            data = {f"{uniName, collegeName}" : articulation_dict}
            
            """ 
            HACK Create file on writing to it
            """
            fileName = "EECS_BERKELEY.json"
            
            # Load existing data from file
            with open(fileName, "r") as file:
                existing_data = json.load(file)
                
            # Merge data from new to old
            existing_data.update(data)
            
            with open(fileName, "w") as file:
                json.dump(existing_data, file, indent=4)
                print("Added new data to file")
                
        except Exception as e:
            print(e)
         
    def quit(self):
        self.driver.quit()
        
if __name__ == "__main__":
    """ 
    Testing:
    major = 32 is EECS major
    institution = 113 is sacramento city college
    institution = 57 is diablo valley
    agreement = 26 is uc berkeley
    """
    bot = WebBot()
    bot.open_articulation_agreements(57, 26) # institution = 113, agreement = 26
    bot.scrape_articulations(32)  
    time.sleep(4)
    bot.quit()
    