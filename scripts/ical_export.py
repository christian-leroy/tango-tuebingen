import json
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz
import re
from pathlib import Path


TZ = pytz.timezone("Europe/Berlin")


def createLocation(milonga) -> str:
    """
    Creates the location as one string, such as: "Tanz-Atelier, Provenceweg 22, 72072 Tübingen"
    """
    location: str = (milonga["venue"] + ", "
        + milonga["street"] + " " + milonga["house_number"] + ", "
        + milonga["postal_code"] + " " + milonga["city"])

    return location


def createUid(milonga) -> str:
    """
    Creates a unique id as DATE + TITLE + @tangotuebingen.de. See test cases for some examples.
    """
    uid: str = milonga["date"] + "-" + milonga["title"] + "@tangotuebingen.de"
    uid = uid.replace(" ", "-")
    uid = re.sub(r"[^a-zA-Z0-9\-\.@]", "", uid)
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
    Creates the description as one string, such as: "DJ Urban – traditionell\nhttps://tangotuebingen.de"
    """
    desc: str = milonga["dj"] + " – " + milonga["style"] + "\nhttps://tangotuebingen.de"

    return desc


def createEventFromMilonga(milonga) -> Event:
    """
    Creates an icalendar event.
    """
    location: str = createLocation(milonga)
    uid: str = createUid(milonga)
    desc: str = createDescription(milonga)
    start_time: datetime = createStartTime(milonga)
    end_time: datetime = createEndTime(milonga)

    event = Event()
    event.add('dtstamp', datetime.now(TZ))
    event.add('dtstart', start_time)
    event.add('dtend', end_time)
    event.add('summary', milonga["title"])
    event.add('location', location)
    event.add('uid', uid)
    event.add('description', desc)
    event.add('url', "https://tangotuebingen.de")
    event.add('sequence', 0)

    return event


def getOldCalendar(calendar_path: Path) -> dict[str, Event] | None:
    """
    Reads the existing .ics file and returns a dictionary of events with uid as key.
    """
    if not calendar_path.exists():
        return None

    with open(calendar_path, "rb") as file:
        old_calendar = Calendar.from_ical(file.read())

    return {str(e.get("uid")): e for e in old_calendar.walk() if e.name == "VEVENT"}


def eventWasChanged(old: Event, new: Event) -> bool:
    """
    Compares every field of two events and returns true if there is a difference in at least one field.
    """
    for prop in new:
        if prop in ("SEQUENCE", "DTSTAMP"):
            continue
        if new[prop] != old.get(prop):
            return True
    return False


def createCalendarFromJSON(milonga_path: Path, calendar_path: Path) -> Calendar:
    """
    Iterates over all JSON entries and creates one ics-event per entry.
    """
    cal = Calendar()
    cal.add('prodid', '-//Tango Tübingen//Milonga//DE')
    cal.add('version', '2.0')

    old_cal = getOldCalendar(calendar_path)

    with open(milonga_path, "r") as file:
        data = json.load(file)
        for milonga in data:
            event = createEventFromMilonga(milonga)
            
            # Check if this event already exists
            if old_cal is not None:
                uid = str(event.get("uid"))
                existing_event = old_cal.get(uid)
                
                # Increment sequence if this event is an update of an existing event
                if existing_event is not None:
                    old_seq = existing_event.get("sequence", 0)
                    if eventWasChanged(existing_event, event):
                        event["sequence"] = old_seq + 1
                    else:
                        event["sequence"] = old_seq

            cal.add_component(event)

    return cal

def writeCalendarAsIcs(milonga_path: Path, calendar_path: Path):
    cal = createCalendarFromJSON(milonga_path, calendar_path)
        
    # Write .ics
    calendar_path.parent.mkdir(parents=True, exist_ok=True)
    with open(calendar_path, 'wb') as f:
        f.write(cal.to_ical())


def main():
    milongas = Path(__file__).parent.parent / "data" / "milongas.json"
    calendar = Path(__file__).parent.parent / "milongas-tue.ics"
    writeCalendarAsIcs(milongas, calendar)

if __name__ == "__main__":                                                                                                       
    main()                                                                                                                       