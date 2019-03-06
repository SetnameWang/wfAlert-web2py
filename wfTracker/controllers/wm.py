# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
import wmPricing

def index():
    return dict(
    )

def api():
    nameUrl = request.vars.nameUrl
    if nameUrl is None:
        api = {'list': [], 'upTime': 0}
        temp['userName'] = 'Null'
        temp['quantity'] = 0
        temp['platinum'] = 0
        api['list'].append(temp)
    else : api = wmPricing.search(nameUrl)
    if len(api['list']) == 0: api['list'].append({'userName': 'Null', 'quantity': 0, 'platinum': 0})
    return dict(
    api=api,
    )
