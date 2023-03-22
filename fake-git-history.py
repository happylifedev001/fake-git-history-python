#! /usr/bin/env python

import subprocess
import shutil
import os
from datetime import datetime, timedelta, date
import random
import argparse

def getDateList(s:date, e:date, w_freq:tuple, d_freq:tuple, workday:bool) -> list:
    res_list = []
    current_day = s 
    
    # current_weekday =  current_day.weekday()
    # delta_days = (7 - current_weekday) % 7
    # current_day += timedelta(days=delta_days)

    while True:        
        # select days
        next_week_date = current_day + timedelta(days=7)
        week_days = random.sample(range(5 if workday else 7), random.randint(*w_freq))
        for days in sorted(week_days):
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

def make_commit_history(start_date:date, end_date:date, weekly_commit=(1,5), day_commit = (0,3), workday=False):
    
    print('make local repository')
    dir_name = 'my-history'    
    # check directory
    if os.path.exists(dir_name):
        os.rmdir(dir_name)
    os.mkdir(dir_name)
    os.chdir(dir_name)
    print('=== Git History Create ===')
    subprocess.run(["git", "init"])
    print("Creating history...")
    # make datetime list
    date_list = getDateList(start_date, end_date, weekly_commit, day_commit, workday)
    for date in date_list:
        date_string = date.isoformat()
        # create a file
        with open('my_file.txt', 'wt', encoding='utf-8') as f:
            f.write('hello git :')
            f.write(date_string)
        
        commit_message = random.choice(['add file via upload', 'modify a func', 'delete file'])

        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", f"--date={date_string}", "-m", f"{commit_message}", "--quiet"])
    print(f"=== finished (commits:{len(date_list)}, {date_list[0]}-{date_list[-1]}) ===")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--startDate", default=None, help="start date for git history. default: a year ago from now")
    parser.add_argument("-e", "--endDate", default=None, help="start date for git history. default: a year ago from now")
    parser.add_argument("-w","--weelyFreq", default='3..5', help="the range of number of days commiting in a week")
    parser.add_argument("-c","--commitPerDay", default='0..3', help="the range of number of commits per day")
    parser.add_argument("-wd", "--workdaysOnly", action="store_true", help="commit in only workdays")

    args = parser.parse_args()
    
    end_date =  date.today() if args.endDate is None else date.fromisoformat(args.endDate)
    start_date =  date(end_date.year - 1, end_date.month, end_date.day) if args.startDate is None else date.fromisoformat(args.startDate)
    workdays_flag = args.workdaysOnly
    weekly_freq = tuple(map(int, args.weelyFreq.split('..')))
    commit_day= tuple(map(int , args.commitPerDay.split('..')))

    make_commit_history(start_date, end_date, weekly_freq, commit_day, workdays_flag)
