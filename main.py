# importing necessary packages 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

"""
XPath Cheat Sheet = "https://quickref.me/xpath"
Assist.org = "https://assist.org"
Extra websites = " "
"""

# # for holding the resultant list 
# page_url = "https://assist.org"
# options = Options()
# options.add_experimental_option("detach", True) # So browser don't close prematurely
# driver = webdriver.Chrome(options=options)
# driver.get(page_url)

class WebBot():
    
    def __init__(self):
        
        print("Initializing WebBot...")
        
        options = Options()
        options.add_experimental_option("detach", True) # So browser don't close prematurely
        options.add_argument("--window-size=1920,1080")  # Adjust the width and height as needed
        self.driver = webdriver.Chrome(options=options)
        self.url = "https://assist.org"
        print("Initialized finished...")
        
    def open_articulation_agreements(self):
        
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
            institution = driver.find_element(By.XPATH, "//div[contains(@id, '-113') and @class='ng-option' and @role='option']/span[@class='ng-option-label']")
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
            agreement = driver.find_element(By.XPATH, "//div[contains(@id, '-26') and @class='ng-option' and @role='option']/span[@class='ng-option-label']")
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
            
    def quit(self):
        self.driver.quit()
        
        
        
if __name__ == "__main__":
    bot = WebBot()
    bot.open_articulation_agreements()
    print("Now scraping")
    bot.scrape_articulations(32)
    print("Found 32")   
    