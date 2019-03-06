# -*- coding: utf-8 -*-

import json
import urllib3
import ssl
import time


#wm查询:
def wmPricing(name):
    print('download infomation...')
    url = 'https://api.warframe.market/v1/items/' + name + '/orders'
    print(url)
    https = urllib3.PoolManager()
    req = https.request(
        'GET',
        url,
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        },
    )
    data = req.data.decode()
    print('download complate...')
    data = json.loads(data)
    data = data['payload']['orders']
    seller = []
    for element in data:
        if element['user']['status'] == 'ingame' and element['order_type'] == 'sell': seller.append(element)
    for i in range(0,20):
        for j in range(0,len(seller)-1):
            if seller[j]['platinum'] <= seller[j+1]['platinum']: seller[j+1], seller[j] = seller[j], seller[j+1]
    data = seller[len(seller)-20:]
    tempList = []
    temp = {}
    for element in data:
        temp = {}
        temp['userName'] = element['user']['ingame_name']
        temp['quantity'] = element['quantity']
        temp['platinum'] = element['platinum']
        tempList.append(temp)
    data = tempList[::-1]
    localData[name] = {}
    localData[name]['list'] = data
    localData[name]['upTime'] = time.time()
    return localData[name]
    #订单数据:data['payload']['orders']
	
#本地存储查询
def search(name):
    try:
        if int(localData[name]['upTime'] - time.time()) > -600:
            return localData[name]
        else:
            return wmPricing(name)
    except:
        return wmPricing(name)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
localData = {}
