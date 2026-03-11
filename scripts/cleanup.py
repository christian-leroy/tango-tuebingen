import json
from pathlib import Path
import datetime as dt
from enum import Enum                                                                                                            

def isOver(date: str, today: dt.date) -> bool:
    """Calculates if a date is in the past. If date == today returns false!

    Args:                                                                                                                            
        date: Date string in YYYY-MM-DD format.
    """
    date = dt.datetime.strptime(date, "%Y-%m-%d").date()
    diff = date - today
    diff = diff.total_seconds()
    
    return diff < 0


def filterMilongas(milongas: Path, today: dt.date):
    """
    Returns 
    Args:
        milongas: Path to milongas.json.
        today: Datetime object of today's date.
    """
    with open(milongas) as file:
        data = json.load(file)
        old = []
        current = []

        for milonga in data:
            if isOver(milonga["date"], today):
                old.append(milonga)
            else:
                current.append(milonga)
        
        return old, current


def main():
    milongas = Path(__file__).parent.parent / "data" / "milongas.json"
    archive = Path(__file__).parent.parent / "data" / "archive.json"
    today = dt.date.today()

    if not archive.exists():
        archive.write_text("[]")

    # Step 1: Update archive with all milongas that are in the past (excluding today)
    old_milongas, current_milongas = filterMilongas(milongas, today)

    with open(archive) as file:
        data = json.load(file)
        data = data + old_milongas
        data.sort(key=lambda milonga: milonga["date"])

    with open(archive, "w") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    # Step 2: Update milongas to only include milongas that are in the future or today
    current_milongas.sort(key=lambda milonga: milonga["title"])
    with open(milongas, "w") as file:
        json.dump(current_milongas, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":                                                                                                       
    main()                                                                                                                       
