from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import json
import time

# Text to speech, just for demo purposes
from tts import speak
"""
TODO: Search "All Majors" instead of EECS for now
    : Add "And" / "Or" to with both sides of articulations

XPath Cheat Sheet = "https://quickref.me/xpath"
Assist.org = "https://assist.org"
Extra websites = " "
"""
class WebBot():
    
    def __init__(self):
        
        speak("Initializing WebBot...")
        
        options = Options()
        options.add_experimental_option("detach", True) # So browser don't close prematurely
        options.add_argument("--window-size=1440,960")  # Adjust the width and height as needed
        self.driver = webdriver.Chrome(options=options)
        self.url = "https://assist.org"
        speak("Initialized finished...")
            
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
            
            # select College
            agreement = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[contains(@id, '-{agreement_num}')]"))
            )
            actions.move_to_element(agreement).click().perform()
            # agreement.click()
            
            # Click on agreement HACK
            driver.find_element(By.XPATH, "/html/body/app-root/div[2]/app-home-component/section[@class='content']/app-form-container/div[@class='formArea']/div[@id='agreementInformationForm']/app-transfer-agreements-form/div[@class='panel agreements']/div[@class='panel-content']/form[@id='transfer-agreement-search']/div[@class='d-flex justify-content-center']/button[@class='btn btn-primary']").click()
            
        except Exception as e:
            speak(f"Error on page 1: {e}")
            self.driver.quit()
            return
        
    # EECS: //div[@class='viewByRow'][32]
    def scrape_articulations(self, major):
        """ 
        Args:
        major: Int
        
        Output:
        data: Dict
        """
        driver = self.driver
        actions = ActionChains(driver)
        try:
            chooseMajor = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[@class='viewByRow'][{major}]"))
            )
            actions.move_to_element(chooseMajor).click().perform()
        except Exception as e:
            speak(e)
            driver.quit()
            return
        
        """
        Key: MATH1A, Value: MATH400 ("Sacramento City College"), MATH400 ("American River College")
        e.g.
        
        Agreement = UNI + "<->" + COLLEGE
        
        { 
            "Berkeley, Sacramento City College" : { "MATH1A" : "MATH400" }
        }
        """
        time.sleep(1)
        try:
            uniName = driver.find_element(By.XPATH, "//div[@class='instReceiving']/p[@class='inst']").text
            collegeName = driver.find_element(By.XPATH, "//div[@class='instSending']/p[@class='inst']").text
            majorName = driver.find_element(By.XPATH, "//div[@class='resultsBoxHeader']/h1").text
            
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
            
            data = {f"{uniName, collegeName}" : (majorName, articulation_dict)}
            
            return data
        
        except Exception as e:
            speak(e)
            return 0
         
    def quit(self):
        self.driver.quit()
        
        
        
# Create a separate writing to file function
def write_data_to_file(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    try:
        with open(file_path, "r") as file:
            existing_data = json.load(file)
    except:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
            speak("Added new data to file")
            
            return 0
        
    # Merge data from new to old
    existing_data = {}
    existing_data.update(data)
    
    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=4)
        speak("Added new data to file")
        
        
if __name__ == "__main__":
    """ 
    Testing:
    Insitution = 136 (UCB)
    Agreement = 106 (SCC)
    Major = 32 (EECS)
    """
    bot = WebBot()
    file_name = "data_files/EECS_BERKELEY.json"
    bot.open_articulation_agreements(136, 106) # institution = 136, agreement = 106
    data = bot.scrape_articulations(32)
    write_data_to_file(file_name, data)
    time.sleep(4)
    bot.quit()
    speak("Exited chrome driver")
    
