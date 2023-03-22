#! /usr/bin/env python
import subprocess
import shutil
import os
from datetime import datetime, timedelta
import random

def getDateList(s:datetime, e:datetime, w_freq:tuple, d_freq:tuple) -> list:
    res_list = []
    current_day = s    
    
    # current_weekday =  current_day.weekday()
    # delta_days = (7 - current_weekday) % 7
    # current_day += timedelta(days=delta_days)

    while True:        
        # select days
        next_week_date = current_day + timedelta(days=7)
        week_days = random.sample(range(7), random.randint(*w_freq))
        for days in week_days:
            commit_hours = random.sample(range(9, 20), random.randint(*d_freq))
            current_day += timedelta(days)
            
            if current_day >= e:
                break
            
            for hour in commit_hours:
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                commit_datetime = datetime(current_day.year, current_day.month, current_day.day, hour, minute, second)
                res_list.append(commit_datetime)
        
        current_day = next_week_date
        if current_day >= e:
            break
    return res_list

def make_commit_history(start_date:datetime, end_date:datetime, weekly_commit=(1,5), day_commit = (0,3)):
    
    dir_name = 'my-history'    
    # check directory
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.mkdir(dir_name)
    os.chdir(dir_name)

    subprocess.run(["git", "init"])

    # make datetime list
    date_list = getDateList(start_date, end_date, weekly_commit, day_commit)
    for date in date_list:
        date_string = date.isoformat()
        # create a file
        with open('my_file.txt', 'wt', encoding='utf-8') as f:
            f.write('hello git :')
            f.write(date_string)
        
        commit_message = random.choice(['add file via upload', 'modify a func', 'delete file'])

        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", f"--date={date_string}", "-m", f"{commit_message}"])

    

if __name__ == "__main__":
    
    make_commit_history(
        datetime(2023, 3, 10),
        datetime(2023, 4, 1),
        (1, 5),
        (0, 3))
