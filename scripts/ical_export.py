import json
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz
import re
from pathlib import Path


TZ = pytz.timezone("Europe/Berlin")            

"""


  
  from icalendar import Calendar, Event
  from datetime import datetime

  cal = Calendar()
  cal.add('prodid', '-//Tango Tübingen//Milonga//DE')
  cal.add('version', '2.0')

  event = Event()
  event.add('summary', 'Milonga im Sudhaus')
  event.add('dtstart', datetime(2026, 3, 15, 20, 0, 0))
  event.add('dtend', datetime(2026, 3, 15, 23, 0, 0))
  event.add('location', 'Sudhaus, Tübingen')
  event.add('uid', 'milonga-20260315@tangotübingen.de')

  cal.add_component(event)

  Datei schreiben

  cal.to_ical() gibt bytes zurück (bereits CRLF-terminiert, korrekt gefoldet und escaped):

  with open('milongas.ics', 'wb') as f:
      f.write(cal.to_ical())

  """

def createLocation(milonga) -> str:
    """
    Creates the location as one string, such as: "Tanz-Atelier, Provenceweg 22, 72072 Tübingen"
    """
    location: str = (milonga["venue"] + ", " 
    + milonga["street"] + " " + milonga["house_number"] + ", "
    + milonga ["postal_code"] + " " + milonga["city"])

    return location


def createUid(milonga) -> str:
    """
    Creates a unique id as DATE + TITLE + @tangotuebingen.de. See test cases for some examples.
    """
    uid: str = milonga["date"] + "-" + milonga["title"] + "@tangotuebingen.de"  
    uid = uid.replace(" ", "-") # turns spaces into -
    uid = re.sub(r"[^a-zA-Z0-9\-\.@]", "", uid) # removes all non-standard symbols
    uid = re.sub(r"-+", "-", uid)                                                                                             

    return uid 

def createStartTime(milonga) -> datetime:
    """
    Creates the start time.
    """
    dt = datetime.strptime(f"{milonga['date']} {milonga['start_time']}", "%Y-%m-%d %H:%M")
    return TZ.localize(dt)


def createEndTime(milonga) -> datetime:
    """
    Creates the end time. Handles 24:00 edge case.
    """
    if milonga["end_time"] == "24:00":
        dt = datetime.strptime(f"{milonga['date']} 00:00", "%Y-%m-%d %H:%M") + timedelta(days=1)
    else:
        dt = datetime.strptime(f"{milonga['date']} {milonga['end_time']}", "%Y-%m-%d %H:%M")
    return TZ.localize(dt)


def createDescription(milonga) -> str:
    """
    Creates the description as one stirng, such as: "DJ Urban – traditionell"
    """
    desc: str = milonga["dj"] + " – " + milonga["style"]
    
    return desc


def createEventFromMilonga(milonga) -> Event:
    """
    Creates an icalendar event.
    """

    # Compute information
    location: str = createLocation(milonga)
    uid: str = createUid(milonga)
    desc: str = createDescription(milonga)
    start_time: datetime = createStartTime(milonga)
    end_time: datetime = createEndTime(milonga)

    # Add all fields to event
    event = Event()
    event.add('dtstamp', datetime.now(TZ))
    event.add('dtstart', start_time)
    event.add('dtend', end_time)
    event.add('summary', milonga["title"])
    event.add('location', location)
    event.add('uid', uid)
    event.add('description', desc)
    event.add('url', "https://tangotuebingen.de")

    return event


def main():
    milongas = Path(__file__).parent.parent / "data" / "milongas.json"
    calendar = Path(__file__).parent.parent / "calendar" / "milongas.ics"

    # Setup calendar object
    cal = Calendar()
    cal.add('prodid', '-//Tango Tübingen//Milonga//DE')
    cal.add('version', '2.0')

    # Fetch milongas, create events, add them to calendar
    with open(milongas, "r") as file:
        data = json.load(file)
        for milonga in data:
            event = createEventFromMilonga(milonga)
            cal.add_component(event)
    
    # Write .ics
    calendar.parent.mkdir(parents=True, exist_ok=True)
    with open(calendar, 'wb') as f:
      f.write(cal.to_ical())

if __name__ == "__main__":                                                                                                       
    main()                                                                                                                       