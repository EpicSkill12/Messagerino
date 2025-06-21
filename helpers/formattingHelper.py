from datetime import datetime

def formatTime(time: float):
    dateTime = datetime.fromtimestamp(time)
    return dateTime.strftime(r"%d.%m.%Y - %H:%M Uhr")