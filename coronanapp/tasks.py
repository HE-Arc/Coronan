from background_task import background
from django.contrib.auth.models import User
from .models import Profile, Bet
import urllib.request, json
from datetime import date, timedelta, datetime

@background(schedule=5)
def hourly_fetch():
    UpdateAllBets()

def UpdateAllBets():
    bets = Bet.objects.all()
    last_sunday = date.today()
    while last_sunday.weekday() != 6:
        last_sunday = last_sunday - timedelta(1)
    betThisWeek = []
    for bet in bets:
        delta = 0
        if bet.date:
            delta = (bet.date - last_sunday).days
        if delta > 0:
            betThisWeek.append(bet)
    for bet in betThisWeek:
        print(bet.date)

    #print(bets)
    #print(bets[0].date)
    #print(type(bets[0].date))


def getcasesAtDate(theDate, data):
    result = {}
    for elem in data["data"]["timeline"]:
        if str(elem["date"]) == str(theDate):
            result = elem
    return result

#6 dimanche, 5 samedi, ... 0 lundi
def getWeekCases(theDate, weekDay):
    url = "https://corona-api.com/countries/ch"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    today = theDate
    total = 0

    total += getcasesAtDate(today.strftime("%Y-%m-%d"), data)["new_confirmed"]
    print(today)
    print(today.weekday())
    
    today = today - timedelta(1)
    while(today.weekday() != 6):
        print(today)
        print(today.weekday())
        try:
            total += getcasesAtDate(today.strftime("%Y-%m-%d"))["new_confirmed"]
        except:
            total += 0
        today = today - timedelta(1)

    return total