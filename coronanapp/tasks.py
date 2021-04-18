from background_task import background
from django.contrib.auth.models import User
from .models import Profile, Bet
import urllib.request, json
from datetime import date, timedelta, datetime

@background(schedule=5)
def hourly_fetch():
    UpdateAllBets()

def UpdateAllBets():
    todayDate = date(2021, 4, 11)
    bets = Bet.objects.all()
    last_sunday = todayDate
    while last_sunday.weekday() != 6:
        last_sunday = last_sunday - timedelta(1)
    betThisWeek = []
    for bet in bets:
        delta = 0
        if bet.date:
            delta = (bet.date - last_sunday).days
        if delta > 0:
            betThisWeek.append(bet)
    moneySum = sum(bet.moneyBet for bet in betThisWeek)
    ponderationDict = {}
    for bet in betThisWeek:
        betDate = abs(bet.date.weekday()-6)
        ponderationDict[bet.pk] = (betDate * bet.moneyBet) / (moneySum * abs(bet.cases-getWeekCases(todayDate)))
    ponderationSum = 0
    for pond in ponderationDict:
        ponderationSum += ponderationDict[pond]
    for bet in betThisWeek:
        bet.moneyWon = (ponderationDict[bet.pk] / ponderationSum) * moneySum
        bet.status = "Validated"
        bet.save()
        profile = Profile.objects.get(user=bet.user.pk)
        print("\n\nPARIEUR : " + str(bet.user) + "\n")
        print("ARGENT GAGNÉ : " + str(bet.moneyWon))
        print("ARGENT AVANT : " + str(profile.funds))
        profile.funds += bet.moneyWon
        profile.save()
        print("ARGENT APRÈS : " + str(profile.funds))
        print("PONDERATION : " + str(ponderationDict[bet.user.pk]))
    print(ponderationSum)
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
def getWeekCases(theDate):
    url = "https://corona-api.com/countries/ch"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    today = theDate
    total = 0

    total += getcasesAtDate(today.strftime("%Y-%m-%d"), data)["new_confirmed"]
    
    today = today - timedelta(1)
    while(today.weekday() != 6):
        try:
            total += getcasesAtDate(today.strftime("%Y-%m-%d"))["new_confirmed"]
        except:
            total += 0
        today = today - timedelta(1)

    return total