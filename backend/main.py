from webBot import WebBot
from webBot import write_data_to_file
import time
import os
import json
if __name__ == "__main__":
    """ 
    Testing:
    major = 32 is EECS major
    institution = 113 is sacramento city college
    institution = 57 is diablo valley
    agreement = 26 is uc berkeley
    """
    bot = WebBot()
    file_name = "data_files/EECS_BERKELEY.json"
    bot.open_articulation_agreements(113, 26) # institution = 113, agreement = 26
    data = bot.scrape_articulations(32)
    write_data_to_file(file_name, data)
    time.sleep(4)
    bot.quit()
    
