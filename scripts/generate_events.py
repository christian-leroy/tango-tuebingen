import json
import datetime as dt
from datetime import timedelta
from pathlib import Path

def daysUntilWeekday(baseline_weekday: int, event_weekday: int) -> int:
    """Returns the number of days from baseline_weekday to the next occurrence of event_weekday (1–7).
    Weekdays are integers 0 (Monday) to 6 (Sunday). Same weekday returns 7."""
    
    if baseline_weekday == event_weekday:
        return 7
    
    diff: int = baseline_weekday - event_weekday
    if diff < 0:
        return abs(diff)
    else:
        return 7-diff
    

def nextDate(milonga_template, baseline: dt.date) -> dt.date:
    """Calculates the next occurrence date for a recurring event based on a given baseline date."""
    # Extract relevant information
    baseline_weekday = baseline.weekday()    
    recurrence = milonga_template["recurrence"]
    event_weekday = milonga_template["weekday"]

    # Weekly Case
    if recurrence == "weekly":
        days_offset = daysUntilWeekday(baseline_weekday, event_weekday)
        next_day = baseline + timedelta(days = days_offset)
        return next_day
        
    # TODO: Monthly case
    else:
        raise NotImplementedError


def createNextMilonga(milonga_template: dict, baseline: dt.date) -> dict:
    """Creates a single event dict for the next occurrence of a template from the given baseline."""
   
    next_date = nextDate(milonga_template, baseline).isoformat()
    milonga = {
        "title": milonga_template["title"],
        "date": next_date,
        "dj": milonga_template["dj"],
        "style": milonga_template["style"],
        "start_time": milonga_template["start_time"],
        "end_time": milonga_template["end_time"],
        "venue": milonga_template["venue"],
        "street": milonga_template["street"],
        "house_number": milonga_template["house_number"],
        "postal_code": milonga_template["postal_code"],
        "city": milonga_template["city"],
        "organizer": milonga_template["organizer"],
        "organizer_url": milonga_template["organizer_url"],
        "price": milonga_template["price"],
        "currency": milonga_template["currency"],
        "event_type": milonga_template["event_type"],
        "url": milonga_template["url"],
        "description": milonga_template["description"]
    }

    return milonga


def createRegulars(milonga_templates: list[dict], days: int) -> list[dict]:
    """Creates all occurrences for the given templates within the next `days` days."""
    milongas = []

    for template in milonga_templates:
        start_date: dt.date = dt.date.today()
        stop_date: dt.date = start_date + timedelta(days)
        next_date: dt.date = nextDate(template, start_date)

        while next_date <= stop_date:
            milonga = createNextMilonga(template, start_date)
            milongas.append(milonga)
            start_date = next_date
            next_date = nextDate(template, next_date)
    return milongas            

def main():
    templates = Path(__file__).parent.parent / "data" / "templates.json"
    milongas = Path(__file__).parent.parent / "data" / "milongas.json"
    days = 14

    # Load templates and create all milongas
    with open(templates) as file:
        data = json.load(file)
        # Remove everything that is not weekly for now
        weekly = [t for t in data if t["recurrence"] == "weekly"]
        next_milongas = createRegulars(weekly, days)

    with open(milongas, "r") as file:
        existing_milongas = json.load(file)

    # Make sure the milongas don't exist already
    for milonga_to_add in next_milongas:
        seen = False
        for existing_milonga in existing_milongas:
            if existing_milonga["title"] == milonga_to_add["title"] and existing_milonga["date"] == milonga_to_add["date"]:
                seen = True
        if not seen:
            existing_milongas.append(milonga_to_add)
            print(f"Created {milonga_to_add["title"]} at {milonga_to_add["date"]}") 

    with open(milongas, "w") as file:
        json.dump(existing_milongas, file, indent=2, ensure_ascii=False)

                

if __name__ == "__main__":                                                                                                       
    main()                                                                                                                       
 