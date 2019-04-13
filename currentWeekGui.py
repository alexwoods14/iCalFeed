#!/usr/bin/env python3
import requests
from iCal import iCal
from event import event
import sys
from datetime import datetime, date, timedelta, time
from tkinter import Tk, Canvas

def draw(canv, event):
        colour = "#FFF" # white as standard
        course = event[0]
        eventType = event[1]
        location = event[2][:20] #20 max

        if "Lecture" in eventType:
            colour = "#2EF"
        if "Laboratory" in eventType:
            colour = "#2BF"
        if "Tutorial" in eventType:
            colour = "#29F"
        if "Example" in eventType:
            colour = "#2BC"
        if "Pass" in eventType:
            colour = "#8FF"

        day = event[5]
        start = event[3].hour + event[3].minute/60
        duration = "{} - {}".format(event[3].isoformat(timespec='minutes'), event[4].isoformat(timespec='minutes'))
        end = event[4].hour + event[4].minute/60
        

        midx = xb + day*w + w*0.5 # mid x of box
        y1 = yb + (start - 9)*h + 0.2*h
        y2 = yb + (start - 9)*h + 0.4*h
        y3 = yb + (start - 9)*h + 0.6*h
        y4 = yb + (start - 9)*h + 0.8*h

        relativeHour = (now.hour + now.minute/60)

        Canvas.create_rectangle(canv,xb + day*w, yb + (start - 9)*h, xb + (day+1)*w, yb+ (end - 9)*h, outline="#000", fill=colour)# ,stipple='gray25')

        if displayWeek < currentWeek:
            Canvas.create_rectangle(canv,xb + day*w, yb + (start - 9)*h, xb + (day+1)*w, yb+ (end - 9)*h, outline="#000", fill="#888")
        elif displayWeek == currentWeek: 
            if day < today.weekday():
                Canvas.create_rectangle(canv,xb + day*w, yb + (start - 9)*h, xb + (day+1)*w, yb+ (end - 9)*h, outline="#000", fill="#888")
            elif day == today.weekday() and start < relativeHour:
                if end < relativeHour:
                    Canvas.create_rectangle(canv,xb + day*w, yb + (start - 9)*h, xb + (day+1)*w, yb+ (end - 9)*h, outline="#000", fill="#888")
                else:
                    Canvas.create_rectangle(canv,xb + day*w, yb + (start - 9)*h, xb + (day+1)*w, yb+ (relativeHour - 9)*h, outline="#000", fill="#888")




        Canvas.create_line(canv, xb + today.weekday()*w, yb + (relativeHour - 9)*h, (today.weekday() + 1)*w + xb, yb + (relativeHour - 9)*h)

        Canvas.create_text(canv,midx, y1, text=course) 
        Canvas.create_text(canv,midx, y2, text=eventType)
        Canvas.create_text(canv,midx, y3, text=location)
        Canvas.create_text(canv,midx, y4, text=duration)


def main():
    if("http" in sys.argv[1]):
        data = requests.get(sys.argv[1]).text# url is http feed
    else:
        with open(sys.argv[1], 'r') as content_file:
            data = content_file.read()

    cal = iCal(data)
    
    
    #MyManchester week 0 is 17th Sept 2018
    weekZero = date(2018,9,17)
    global today
    today = date.today()
    global now
    now = datetime.now().time()
    print("current timetable week: ",((today - timedelta(days=today.weekday())) - weekZero).days/7)
    global currentWeek
    currentWeek = int(((today - timedelta(days=today.weekday())) - weekZero).days/7)
    global displayWeek
    displayWeek = currentWeek
    weekToShow = cal.inWeek(displayWeek)

    global h 
    global w 
    global xb
    global yb
    global td
    global th
    
    h = 60 # height of slot
    w = 150 # width of slot
    xb = 50 # x border
    yb = 20 # y border
    td = 5 # total/max days
    th = 10 # total hours

    days = ['Mon','Tue','Wed','Thur','Fri', '']
    
    
    root = Tk()
    canv = Canvas(root, width=td*w + xb, height=th*h + yb)
    canv.pack()

    canv.create_rectangle(xb,yb, td*w + xb, th*h + yb, outline="#000")
    for day in range (0,td + 1): # mon to fri
        canv.create_line(xb + day*w, 0, xb + day*w, yb + h*th)
        canv.create_text(xb + day*w + 0.5*w, yb*0.5, text=days[day])
    for hour in range(9,9+th + 1):
        canv.create_line(0, yb + (hour - 9)*h, td*w + xb, yb + (hour - 9)*h)
        canv.create_text(0.5*xb, yb + (hour - 9)*h + yb*0.5, text="{:02d}00".format(hour))

    
    
    for event in weekToShow:
        draw(canv, event)



    root.mainloop()

main()
