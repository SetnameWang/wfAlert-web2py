# -*- coding: utf-8 -*-
from urllib import request
import json

def getRiven(weapon,weaponType):
    print('request ' + weapon + '...')
    url = 'https://semlar.com/rivencalc/' + weapon + '/' + weaponType
    req = request.Request(url)
    data = request.urlopen(req).read()
    try:
        data = data.decode('utf-8')
    except:
        pass
    print(data)
	
getRiven('cronus','131')