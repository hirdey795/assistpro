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
            agreement = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[contains(@id, '-{agreement_num}')]"))
            )
            actions.move_to_element(agreement).click().perform()
            # agreement.click()
            
            # Click on agreement HACK
            click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//form[@id='transfer-agreement-search']//div[@class='d-flex justify-content-center']/button[@class='btn btn-primary']")))
            actions.move_to_element(click).click().perform()

        except Exception as e:
            print(f"Error on page 1: {e}")
            self.driver.quit()
            return
        
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
                EC.element_to_be_clickable((By.XPATH, f"//div[@class='viewByRow'][{i}+2]/a/div[@class='viewByRowColText']"))
            )
            actions.move_to_element(chooseMajor).click().perform()
        except Exception as e:
            print(e)
            driver.quit()
            return
        
        try:
            #uniName = driver.find_element(By.XPATH, "//div[@class='instReceiving']/p[@class='inst']").text
            #collegeName = driver.find_element(By.XPATH, "//div[@class='instSending']/p[@class='inst']").text
            #majorName = driver.find_element(By.XPATH, "//div[@class='resultsBoxHeader']/h1").text
            waitToLoad = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='resultsBoxHeader']/h1"))
            )
            uniCoursesElements = driver.find_elements(By.XPATH, "//div[@class='rowReceiving']")
            #collegeCoursesElements = driver.find_elements(By.XPATH, "//div[@class='rowContent']/div[@class='articRow isSingle']/div[@class='rowSending node-item node-item--Sending']")
            
            uniCourses = [element.text.split("\n") for element in uniCoursesElements]
            uniCourses = bot.formatUniCourses(uniCourses)
            for i in uniCourses[:]:
                if (("satisfy" in i) or (" " not in i) or ("section" in i)):
                    uniCourses.remove(i)
            print(uniCourses)
            #collegeCourses = [element.text.split("\n")[0] for element in collegeCoursesElements]
            time.sleep(0.5)
            bot.returnToHome()
            #print("----Uni Courses----")
            #print(bot.formatUniCourses(uniCourses))
            #print("----")
            return uniCourses
            #print("----College Courses---")
            #print(collegeCourses)
            #print("----")
            
            #articulation_dict = {uniCourses:collegeCourses for uniCourses, collegeCourses in zip(uniCourses, collegeCourses)}
            
            #data = {f"{uniName, collegeName}" : (majorName, articulation_dict)}
            
            #return data
        
        except Exception as e:
            print(e)
            print("Returning empty list")
            bot.returnToHome()
            return []
    
    def to_tuple(self, courses):
        newTuple = [tuple(l) if isinstance(l, list) else l for l in courses]
        return newTuple
    
    def formatUniCourses(self, uniCourses):
        for i in range(0,len(uniCourses)):
            if "AND" in uniCourses[i]:
                uniCourses[i] = f"{uniCourses[i][0]} AND {uniCourses[i][(uniCourses[i].index("AND")+1)]}"
            else:
                uniCourses[i] = uniCourses[i][0]
        #my_dict = {elements : None for elements in uniCourses}
        return uniCourses

    def quit(self):
        self.driver.quit()
    
    def returnToHome(self): #Return and Come back
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
        

def addNewCourses(data, allCourses, uni):
    #courses = bot.formatUniCourses(courses)
    combined = []
    for course in allCourses:
        combined.extend(course)
    data[uni] = list(set(combined))
    #for i in range(len(allCourses)): 
    #data[uni] =  list(set(allCourses[i] + data[uni])) for i in allCourses 
        #data[uni].clear()
        #data[uni].append(newCourses)
    return data
    #for i in range(len(courses)):
    #    if courses[i] not in data[uni]:
    #        data[uni].append(courses[i])
    #return data

if __name__ == "__main__":
    """ 
    Testing:
    Insitution = 136 (UCB)
    Agreement = 106 (SCC)
    Major = 32 (EECS)
    """
    bot = WebBot()
    file_name = "data_files/uniCourses.json"
    
    
    
    bot.open_articulation_agreements(136, 106) # institution = 136, agreement = 106 
    courseDict = []
    time.sleep(3)
    uni = bot.getUni()
    majors = bot.getMajors()
    allCourses = []
    data = {f"{uni}" : courseDict}
    print("-----University-----")
    print(uni)
    print("--------------------")
    #for i in range(len(majors)):
    #print(i)
    for i in range(len(majors)):
        print(i)
        print(majors[i])
        allCourses.append(bot.scrape_articulations(i)) 
        courseDict = addNewCourses(data, allCourses, uni)
        write_data_to_file(file_name, data)
    #for i in range(2,4):
        
    #data.update(bot.exportMajors(Uni, majors))
    #bot.returnToHome()
    #print(data)
    #uniCourses = bot.scrape_articulations(2)
    #print(uniCourses)
    #data = addNewCourses(uniCourses, data, uni)
    #print(data)
    #write_data_to_file(file_name, data)
    #time.sleep(2)
    bot.quit()
    
