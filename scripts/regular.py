import json
import datetime as dt
import calendar

today = dt.date.today()

def findNextDate(milonga_template, baseline: dt.date):
    # Extract relevant information
    year = baseline.year()
    month = baseline.month()
    day = baseline.day()
    weekday = baseline.weekday()
    
    # Get calendar
    cal = calendar.monthcalendar(baseline)


    recurrence = milonga_template["recurrence"]
    event_weekday = milonga_template["weekday"]
    week_of_month = milonga_template.get("week_of_month", None)

    if recurrence == "weekly":
        delta = weekday - event_weekday

        """
        Baseline monday, scheduled tueday, diff 1 -> baseline +1
        Baseline tuesday, sched monday, 
        """



# date =  milonga_template["date"].dt.datetime.strptime(date, "%Y-%m-%d").date()

"""
1. Take some date as baseline. Define a limit.
2. Find next date from that baseline.
3. If next date <= limit: create event

"""