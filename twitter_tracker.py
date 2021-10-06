import db_funcs as collect_info
import schedule
import time
from config import apiKey
from datetime import date

class Twitter_Tracker:
    def __init__(self, api_key):
        """ assign api key to the object """
        self.api_key = api_key

    def collect(self, from_date, to_date, user):
        """ collect data about the user with the given dates """
        collect_info.insert_fullName(user)        
        collect_info.insert_followers(user)
        collect_info.insert_data_to_DB(from_date, to_date, user)

    
    def view(self, start_date, end_date, user="all"):
        """ Get the list to view it back to the user """
        view_list = collect_info.view_data(start_date, end_date, user)
        return view_list

        #TODO: what if the user equals to all? I never delt with this. 
        #TODO: I should have added an if statement asking if user == "" then we send it to another function that returns 
        #TODO: all the data for all the users.


    def create_scheduler_daily(self):
        """ Code below is to create a scheduler daily """
        users_list = collect_info.fetch_all_users()  # get all the users we currently have in our DB      
        today = date.today()                         # get today's date

        for i in users_list:
            # loop over each user and schedule a process to track their information everyday at 9
            schedule.every().day.at("09:00").do(t.collect, today, today, i)

        while True:
            schedule.run_pending()   # run the function we want to schedule
            time.sleep(60)           # wait one minute

t = Twitter_Tracker(apiKey)  # create an object t with our api key

