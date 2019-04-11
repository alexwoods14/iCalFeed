import re

class event:
    def __init__(self, data):
        self.plain = data
        self.course = data[1].strip("SUMMARY:")
        self.location = data[2].strip("LOCATION:").replace("_",":").replace("\\","")[:-2]
        self.weeks = self.calcWeeks(re.sub(r".*(Weeks)?\:", "",data[4]))
        if "DTSTART" in data[5]:
            self.startTime = calcTime(data[5].strip("DTSTART:"))
            self.endTime = calcTime(data[6].strip("DTEND:"))
        else:
            self.startTime = calcTime(data[6].strip("DTSTART:"))
            self.endTime = calcTime(data[7].strip("DTEND:"))

    def __str__(self):
        return str(self.plain)

    def __repr__(self):
        return str(self)

    def course(self):
        return self.course
    
    def location(self):
        return self.location

    def item(self, idx):
        return self.plain[idx]

    def weeks(self):
        return self.weeks

    def time(self):
        return self.startTime, self.endTime

    def calcWeeks(self, weeksString):
        weeksString = weeksString.replace("\\,","")
        weeksList = weeksString.split(" ")
        final = []
        for week in weeksList:
            if "-" in week: 
                a, b = week.split('-')
                final.extend(map(str, range(int(a), int(b)+1)))
            else:
                final.append(week)

        return final



def calcTime(timeString):
    #implement
    return timeString
