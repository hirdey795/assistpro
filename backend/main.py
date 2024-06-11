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

"""
TODO: Search "All Majors" instead of EECS for now
    : Add "And" / "Or" to with both sides of articulations

XPath Cheat Sheet = "https://quickref.me/xpath"
Assist.org = "https://assist.org"
Extra websites = " "
"""
class WebBot():
    
    def __init__(self):
        
        print("Initializing WebBot...")
        
        options = Options()
        options.add_experimental_option("detach", True) # So browser don't close prematurely
        options.add_argument("--window-size=1440,960")  # Adjust the width and height as needed
        self.driver = webdriver.Chrome(options=options)
        self.url = "https://assist.org"
        print("Initialized finished...")
            
    def open_articulation_agreements(self, institution_num, agreement_num):
        
        driver = self.driver
        actions = ActionChains(driver)
        driver.get(self.url)
        print("Reading data...")
        
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
            print(f"Error on page 1: {e}")
            self.driver.quit()
            return
        
    # EECS: //div[@class='viewByRow'][32]
    # Gets Majors once at agreement page
    def getMajors(self):
        driver = self.driver
        actions = ActionChains(driver)
        try:
            time.sleep(1)
            majorsElements = driver.find_elements(By.XPATH, "//div[@class='viewByRow']/a/div[@class='viewByRowColText']")
            majors = [element.text.split("\n")[0] for element in majorsElements]
            majors.pop(0)
            return majors
        except Exception as e:
            print(e)
            return
    
    def getUni(self):
        driver = self.driver
        actions = ActionChains(driver)
        uni = driver.find_element(By.XPATH, "//div[@class='criteria'][1]/span").text
        return uni
        
    def exportMajors(self, uniName,  majors):
        data = {f"{uniName}" : majors}
        return data
    
    def scrape_articulations(self, i):
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
                EC.element_to_be_clickable((By.XPATH, f"//div[@class='viewByRow'][{i}]/a/div[@class='viewByRowColText']"))
            )
            actions.move_to_element(chooseMajor).click().perform()
        except Exception as e:
            print(e)
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
            #uniName = driver.find_element(By.XPATH, "//div[@class='instReceiving']/p[@class='inst']").text
            #collegeName = driver.find_element(By.XPATH, "//div[@class='instSending']/p[@class='inst']").text
            #majorName = driver.find_element(By.XPATH, "//div[@class='resultsBoxHeader']/h1").text
            
            uniCoursesElements = driver.find_elements(By.XPATH, "//div[@class='rowReceiving']")
            #collegeCoursesElements = driver.find_elements(By.XPATH, "//div[@class='rowContent']/div[@class='articRow isSingle']/div[@class='rowSending node-item node-item--Sending']")
            
            uniCourses = [element.text.split("\n") for element in uniCoursesElements]
            #collegeCourses = [element.text.split("\n")[0] for element in collegeCoursesElements]
                    
            print("----Uni Courses----")
            print(uniCourses)
            print("----")
            return uniCourses
            #print("----College Courses---")
            #print(collegeCourses)
            #print("----")
            
            #articulation_dict = {uniCourses:collegeCourses for uniCourses, collegeCourses in zip(uniCourses, collegeCourses)}
            
            #data = {f"{uniName, collegeName}" : (majorName, articulation_dict)}
            
            #return data
        
        except Exception as e:
            print(e)
            return 0

    def formatUniCourses(self, uniCourses):
        for i in range(0,len(uniCourses)):
            if "AND" in uniCourses[i]:
                uniCourses[i] = [f"{uniCourses[i][0]}", f"{uniCourses[i][(uniCourses[i].index("AND")+1)]}"]
            else:
                uniCourses[i] = uniCourses[i][0]
        return uniCourses


    def quit(self):
        self.driver.quit()
    
    # Clicks on "Modify Search Button"
    def returnToHome(self):
        driver = self.driver
        actions = ActionChains(driver)
        try:
            returnToHome = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div[2]/app-transfer/section[@class='left-panel']/div[@class='logo-lockup']/a[@class='btn btn-primary']"))
                    )
            actions.move_to_element(returnToHome).click().perform()
        except Exception as e:
            print(e)
            driver.quit()
            return
        
        
        
# Create a separate writing to file function
def write_data_to_file(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    try:
        with open(file_path, "r") as file:
            existing_data = json.load(file)
    except:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
            print("Added new data to file")
            
            return 0
        
    # Merge data from new to old
    existing_data = {}
    existing_data.update(data)

    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=4)
        print("Added new data to file")
        
        
if __name__ == "__main__":
    """ 
    Testing:
    Insitution = 136 (UCB)
    Agreement = 106 (SCC)
    Major = 32 (EECS)
    """
    bot = WebBot()
    file_name = "data_files/MAJORS.json"
    uniCourses = []
    data = {}
    #for i in range(10, 29):
        #bot.open_articulation_agreements(i, 0)
        #majors = bot.getMajors()
        #Uni = bot.getUni()
        #data.update(bot.exportMajors(Uni, majors))
        #bot.returnToHome()
    #for i in range(136, 145):
        #bot.open_articulation_agreements(i, 0)
        #majors = bot.getMajors()
        #Uni = bot.getUni()
        #data.update(bot.exportMajors(Uni, majors))
        #bot.returnToHome()

    bot.open_articulation_agreements(136, 106) # institution = 136, agreement = 106 
    #print(data)
    data = bot.scrape_articulations(32)
    uniCourses = bot.formatUniCourses(data)
    print(uniCourses)
    #write_data_to_file(file_name, data)
    time.sleep(4)
    bot.quit()
    
