# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
import eventTracker
import time

def index():
    Alerts = eventTracker.Alerts()
    Sorties = eventTracker.Sorties()
    activeMissions = eventTracker.activeMissions()
    voidTrader = eventTracker.voidTrader()
    invasions = eventTracker.invasions()
    cetusSyndicates = eventTracker.cetusSyndicate()
    dailyDeals = eventTracker.dailyDeals()
    timeNow = int(time.time() - 1531637400)
    timeNow = timeNow - int(timeNow/9000)*9000
    cetusCycle = {}
    if timeNow - 6000 < 0 : 
        cetusCycle['state'] = 'cetusDay'
        cetusCycle['text'] = '白昼'
        timeLeft = int(6000 - timeNow)
        cetusCycle['timeLeft'] = timeLeft + time.time()
    elif timeNow - 3000 >= 0 : 
        cetusCycle['state'] = 'cetusNight'
        cetusCycle['text'] = '夜晚'
        timeLeft = int(9000 - timeNow)
        cetusCycle['timeLeft'] = timeLeft + time.time()
    return dict(
        Alerts=Alerts,
        sortieTitle = Sorties['title'],
        sortieSteps = Sorties['steps'],
        activeMissions = activeMissions,
        voidTrader = voidTrader,
        invasions = invasions,
        cetusCycle = cetusCycle,
        cetusSyndicates = cetusSyndicates,
        dailyDeals = dailyDeals,
    )
