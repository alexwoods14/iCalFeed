from event import event
import datetime
class iCal:

    def __init__(self, data):
        start = datetime.datetime.now()
        self.plain = data
        # save all the data into a list
        self.plainlist = data.splitlines()

        #split this at first occurance of event start for file information
        endOfInfo = self.plainlist.index('BEGIN:VEVENT')
        self.fileInfo = self.plainlist[:endOfInfo]
        self.splitData(endOfInfo)
        print("time taken:(ms) ",(datetime.datetime.now() - start).total_seconds() * 1000)


    def getAll(self):
        return self.plain

    def getList(self):
        return '\n'.join(self.fileInfo)
    
    def splitData(self, start):
        # all data after the file info
        allEventData = splitAtEvent(self.plainlist[start:])
        self.events = []
        for i in allEventData:
            self.events.append(event(i))

    def getEventRaw(self):
        return '\n'.join(["{} in {}".format(event.course(i), event.location(i)) for i in self.events])

    def getEvent(self, index):
        
        return event.details(self.events[index])

    def getEventItem(self, index):
        return '\n'.join([event.item(i, index) for i in self.events])


def splitAtEvent(toSplit):
    listOfSublists = []
    while True:
        try:
            startOfInfo = toSplit.index('BEGIN:VEVENT') +1
            endOfInfo = toSplit.index('END:VEVENT')
            listOfSublists.append(toSplit[startOfInfo:endOfInfo])
            #print(toSplit[startOfInfo:endOfInfo])
            toSplit = toSplit[endOfInfo + 1:]
        except ValueError:
            #EOF so exit the loop and quit the method call
            break
    return listOfSublists


