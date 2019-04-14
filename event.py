import re
import datetime

class event:
    def __init__(self, data):
        #print("1: {}\n2: {}\n3: {}\n4: {}\n5: {}".format(data[1],data[2],data[3],data[4],data[5]))
        self.plain = data
        self.course = data[1].strip("SUMMARY:")
        self.location = data[2].strip("LOCATION:").replace("_",":").replace("\\","")[:-2]
        self.formatDesc(data[3].strip("DESCRIPTION:"))

        # weeks is actually in description but often over runs into 4th line
        if "TZID" in data[4]:
            self.calcWeeks(re.sub(r".*(Weeks)?\:", "",data[3]))
        else:
            self.calcWeeks(re.sub(r".*(Weeks)?\:", "","{}{}".format(data[3],data[4])))


        if "DTSTART" in data[5]:
            self.startTime, self.endTime, self.day = calcTime(data[5].strip("DTSTART:"), data[6].strip("DTEND:"))
        else:
            self.startTime, self.endTime, self.day = calcTime(data[6].strip("DTSTART:"), data[7].strip("DTEND:"))

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
        return (self.startTime.hour + self.startTime.minute/60), (self.endTime.hour + self.endTime.minute/60)

    def day(self):
        return self.day

    def details(self):
        #return "{}: {} \n{}\nWeeks: {}\nfrom {} til {} on day {}".format(self.course, self.description, self.location, self.weeks, self.startTime, self.endTime, self.day) # as string
        return [self.course, self.description, self.location, self.startTime, self.endTime, self.day] # as list

    def calcWeeks(self, weeksString):
        weeksString = weeksString.replace("\\","").replace(" ", "").strip(" ")
        weeksList = weeksString.split(",")
        final = []
        for week in weeksList:
            if "-" in week: 
                a, b = week.split('-')
                final.extend(map(int, range(int(a), int(b)+1)))
            else:
                final.append(int(week))

        self.weeks = final

    def formatDesc(self, desc):
        start = desc.index('\\n')
        end = desc[(start + 2):].index('\\n')
        self.description = desc[start + 2: start + end + 2].capitalize()



def calcTime(startString, endString):
    #implement
    start = datetime.time(int(startString[9:11]), int(startString[11:13]), 0, 0, tzinfo=None)
    end = datetime.time(int(endString[9:11]), int(endString[11:13]), 0, 0, tzinfo=None)
    day = datetime.date(int(startString[:4]), int(startString[4:6]), int(startString[6:8])).weekday()
    return start, end, day
