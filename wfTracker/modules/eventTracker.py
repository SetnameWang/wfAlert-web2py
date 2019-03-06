# -*- coding: utf-8 -*-
'''
版权所有（C） 2017 <SetnameWang>
这一程序是自由软件，你可以遵照自由软件基金会出版的GNU通用公共许可证条款来修改和重新发布这一程序。或者用许可证的第二版，或者（根据你的选择）用任何更新的版本。
发布这一程序的目的是希望它有用，但没有任何担保。甚至没有适合特定目的的隐含的担保。更详细的情况请参阅GNU通用公共许可证。
你应该已经和程序一起收到一份GNU通用公共许可证的副本。如果还没有，
写信给：
The Free Software Foundation, Inc., 675 Mass Ave, Cambridge,
MA02139, USA
还应加上如何和你保持联系的信息。
如果程序以交互方式进行工作，当它开始进入交互方式工作时，使它输出类似下面的简短声明：
Gnomovision 第69版， 版权所有（C） 19XX， 作者姓名，
Gnomovision绝对没有担保。 要知道详细情况，请输入‘show w’。
这是自由软件，欢迎你遵守一定的条件重新发布它，要知道详细情况，
请输入‘show c’。
假设的命令‘show w’和‘show c’应显示通用公共许可证的相应条款。当然，你使用的命令名称可以不同于‘show w’和‘show c’。根据你的程序的具体情况，也可以用菜单或鼠标选项来显示这些条款。
如果需要，你应该取得你的上司（如果你是程序员）或你的学校签署放弃程序版权的声明。下面只是一个例子，你应该改变相应的名称：
Yoyodyne公司以此方式放弃James Harker
所写的 Gnomovision程序的全部版权利益。
，1989.4.1
Ty coon副总裁
这一许可证不允许你将程序并入专用程序。如果你的程序是一个子程序库。
你可能会认为用库的方式和专用应用程序连接更有用。如果这是你想做的事，使用GNU库通用公共许可证代替本许可证。
'''

from urllib import request
import json
from threading import Timer
import wfDict
import time
import os
#from qqbot import qqbotsched


'''

                             _ooOoo_
                            o8888888o
                            88" . "88
                            (| -_- |)
                            O\  =  /O
                         ____/`---'\____
                       .'  \\|     |//  `.
                      /  \\|||  :  |||//  \
                     /  _||||| -:- |||||-  \
                     |   | \\\  -  /// |   |
                     | \_|  ''\---/''  |   |
                     \  .-\__  `-`  ___/-. /
                   ___`. .'  /--.--\  `. . __
                ."" '<  `.___\_<|>_/___.'  >'"".
               | | :  `- \`.;`\ _ /`;.`/ - ` : | |
               \  \ `-.   \_ __\ /__ _/   .-` /  /
          ======`-.____`-.___\_____/___.-`____.-'======
                             `=---='
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     佛祖保佑        永无BUG
'''

#突击函数-webed
def Sorties():
    sortie = {}
    sortie['title'] = str(worldDict[0][worldData['Sorties'][0]['Boss']])
    sortie['steps'] = []
    for i in worldData['Sorties'][0]['Variants']:
        step = {}
        location = i['node']
        try:
            location = wfDict.nodes[location]['name'] + '（' + wfDict.nodes[location]['systemName'] + '）'
            step['missionType'] = worldDict[0][i['missionType']]
        except:
            pass
            step['missionType'] = i['missionType']
        step['location'] = location
        step['modifierType'] = worldDict[0][i['modifierType']]
        sortie['steps'].append(step)
    return sortie

#警报-webed
def Alerts():
    alerts = []
    for i in worldData['Alerts']:
        alert = {}
        location = i['MissionInfo']['location']
        try: 
            location = wfDict.nodes[location]['name'] + '（' + wfDict.nodes[location]['systemName'] + '）'
        except:
            pass
        '''
        location 任务位置
        missionType 任务类型
        level 等级
        item 奖励物品
        crs 现金
        timeLeft 剩余时间
        '''
        alert['location'] = location
        alert['missionType'] = worldDict[0][i['MissionInfo']['missionType']] + ' - ' + worldDict[0][i['MissionInfo']['faction']]
        alert['level'] = '等级:' + str(i['MissionInfo']['minEnemyLevel']) + '-' + str(i['MissionInfo']['maxEnemyLevel'])
        if 'countedItems' in i['MissionInfo']['missionReward']:
            item = i['MissionInfo']['missionReward']['countedItems'][0]['ItemType'].split('/')
            try:
                item = worldDict[0][item[len(item)-1]]
            except:
                item = item[len(item)-1]
            item = item + ' * ' + str(i['MissionInfo']['missionReward']['countedItems'][0]['ItemCount'])
        elif 'items' in i['MissionInfo']['missionReward']:
            item = i['MissionInfo']['missionReward']['items'][0].split('/')
            try:
                item = worldDict[0][item[len(item)-1]]
            except:
                item = item[len(item)-1]
        else:
            item = ''
        alert['items'] = item
        alert['crs'] = '现金:' + str(i['MissionInfo']['missionReward']['credits'])
        alert['timeLeft'] = str(int(int(i['Expiry']['$date']['$numberLong'])/1000))
        alerts.append(alert)
    return alerts

#虚空奸商-webed
def voidTrader():
    voidTrader = {}
    timeLeft = int(worldData['VoidTraders'][0]['Activation']['$date']['$numberLong'])/1000 - int(worldData['Time'])
    if timeLeft > 0:
        voidTrader['state'] = '即将到来'
        voidTrader['timeLeft'] = int(int(worldData['VoidTraders'][0]['Activation']['$date']['$numberLong'])/1000)
    else:
        voidTrader['state'] = '即将离开'
        voidTrader['timeLeft'] = int(int(worldData['VoidTraders'][0]['Expiry']['$date']['$numberLong'])/1000)
    voidTrader['location'] = wfDict.nodes[worldData['VoidTraders'][0]['Node']]['systemName'] + ' 中继站'
    return voidTrader

#战区任务-webed
def invasions():
    invasions = []
    for element in worldData['Invasions']:
        if element['Completed'] == False :
            invasion = {}
            invasion['location'] = wfDict.nodes[element['Node']]['name'] + '(' + wfDict.nodes[element['Node']]['systemName'] + ')'
            invasion['attacker'] = element['AttackerMissionInfo']['faction'].replace('FC_','')
            item = ''
            try:
                if 'countedItems' in element['AttackerReward']:
                    item = element['AttackerReward']['countedItems'][0]['ItemType'].split('/')
                    try: 
                        item = worldDict[0][item[len(item)-1]]
                    except:
                        item = item[len(item)-1]
                    if element['AttackerReward']['countedItems'][0]['ItemCount'] > 1:
                        item = item + ' * ' + str(element['AttackerReward']['countedItems'][0]['ItemCount'])
                elif 'items' in element['AttackerReward']:
                    item = element['AttackerReward']['items'][0].split('/')
                    try: 
                        item = worldDict[0][item[len(item)-1]]
                    except:
                        item = item[len(item)-1]
                else:
                    item = ''
            except:
                pass
            invasion['attackerReward'] = item
            invasion['defender'] = element['DefenderMissionInfo']['faction'].replace('FC_','')
            item = ''
            try:
                if 'countedItems' in element['DefenderReward']:
                    item = element['DefenderReward']['countedItems'][0]['ItemType'].split('/')
                    try:
                        item = worldDict[0][item[len(item)-1]]
                    except:
                        item = item[len(item)-1]
                    if element['DefenderReward']['countedItems'][0]['ItemCount'] > 1:
                        item = item + ' * ' + str(element['DefenderReward']['countedItems'][0]['ItemCount'])
                elif 'items' in element['DefenderReward']:
                    item = element['DefenderReward']['items'][0].split('/')
                    try: 
                        item = worldDict[0][item[len(item)-1]]
                    except:
                        item = item[len(item)-1]
                else:
                    item = ''
            except:
                pass
            invasion['defenderReward'] = item
            invasion['Count'] = element['Count']
            invasion['Goal'] = element['Goal']
            invasion['percent'] = (element['Count'] + element['Goal'])/(element['Goal']*2)
            invasions.append(invasion)
    return invasions

#平原任务-webed
def cetusSyndicate():
    cetusSyndicates = [];
    for element in worldData['SyndicateMissions']['CetusSyndicate'][0]['Jobs']:
        cetusSyndicate = {}
        jobType = element['jobType'].split('/')
        jobType = jobType[len(jobType)-1]
        try:
            jobType = worldDict[0][jobType]
        except:
            pass
        rewards = element['rewards'].split('/')
        rewards = rewards[len(rewards)-1]
        try:
            rewards = worldDict[0][rewards]
            reward = rewards.split('\\n')
            rewards = ''
            for i in reward:
                rewards = rewards + '\n\t' + i
        except:
            pass
        cetusSyndicate['jobType'] = jobType
        cetusSyndicate['level'] = str(element['minEnemyLevel']) + '-' + str(element['maxEnemyLevel'])
        cetusSyndicate['rewards']=''
        cetusSyndicate['copper']=''
        cetusSyndicate['sliver']=''
        cetusSyndicate['gold']=''
        try:
            rewards = rewards.replace('铜：','|||').replace('银：','|||').replace('金：','|||').split('|||')
            cetusSyndicate['copper'] = rewards[1]
            cetusSyndicate['sliver'] = rewards[2]
            cetusSyndicate['gold'] = rewards[3]
        except:
            cetusSyndicate['rewards'] = rewards
        xp = 0
        for num in element['xpAmounts']:
            xp = xp + num
        cetusSyndicate['xp'] = str(xp)
        cetusSyndicates.append(cetusSyndicate)
    return cetusSyndicates


#裂隙-webed
def activeMissions():
    activeMissions = []
    for element in worldData['ActiveMissions']:
        activeMission = {}
        location = element['Node']
        try: 
            activeMission['location'] = wfDict.nodes[location]['name'] + '（' + wfDict.nodes[location]['systemName'] + '）'
            activeMission['missionType'] = str(element['Modifier']).replace('Void','') + ' ' + str(wfDict.nodes[location]['missionType'])
            activeMission['level'] = str(wfDict.nodes[location]['minEnemyLevel']) + '-' + str(wfDict.nodes[location]['maxEnemyLevel'])
        except:
            activeMission['location'] = location
            activeMission['missionType'] = str(element['Modifier']) + ' ' + str(wfDict.nodes[location]['missionType'])
            activeMission['level'] = str(wfDict.nodes[location]['minEnemyLevel']) + '-' + str(wfDict.nodes[location]['maxEnemyLevel'])
        activeMission['timeLeft'] = int(int(element['Expiry']['$date']['$numberLong'])/1000)
        activeMissions.append(activeMission)
    return activeMissions

#每日优惠
def dailyDeals():
    deals = {}
    item = worldData['DailyDeals'][0]['StoreItem'].split('/')
    deals['item'] = item[len(item)-1]
    try:
        deals['item'] = worldDict[0][deals['item']]
    except:
        pass
    deals['timeLeft'] = str(int(worldData['DailyDeals'][0]['Expiry']['$date']['$numberLong'])/1000)
    deals['discount'] = worldData['DailyDeals'][0]['Discount']
    deals['originalPrice'] = worldData['DailyDeals'][0]['OriginalPrice']
    deals['salePrice'] = worldData['DailyDeals'][0]['SalePrice']
    deals['amountTotal'] = worldData['DailyDeals'][0]['AmountTotal']
    deals['amountSold'] = worldData['DailyDeals'][0]['AmountSold']
    return deals
    
#小小黑
def persistentEnemies():
    output = '取名在以下位置追踪到小小黑:'
    for i in worldData['PersistentEnemies']:
        name = i['AgentType'].split('/')
        name = name[len(name)-1]
        location = i['LastDiscoveredLocation']
        try: 
            location = wfDict.nodes[location]['name'] + '（' + wfDict.nodes[location]['systemName'] + '）'
        except:
            pass
        try:
            name = worldDict[0][name]
        except:
            pass
        output = output + '\n\n' + name + ': \n剩余血量: ' + str(round(i['HealthPercent'] * 100, 2)) + '%'
        if i['Discovered'] == True: output = output + '当前状态: 发现\n地点: ' + location
        elif i['Discovered'] == False: output = output + '\n当前状态: 未发现'
    return output



#循环
def timerLoop(inc, updateJson):
    t = Timer(inc, updateJson)
    t.start()

def loadDict():
    #载入词库
    path = os.path.dirname(os.path.realpath(__file__))
    file = open(path + "\worldDATA.txt", "r",encoding= 'utf-8')
    itemDirc = [{},{}]
    for lines in file.readlines():
        lines = lines.rstrip("\n")
        linebar = lines.split('=')
        itemDirc[0][linebar[0]] = linebar[1]
        itemDirc[1][linebar[1]] = linebar[0]
    file.close()
    return itemDirc

#获取JSON文件
def updateJson():
    print('updating world data...')
    url = 'http://content.warframe.com/dynamic/worldState.php'
    req = request.Request(url)
    data = request.urlopen(req).read()
    try:
        data = data.decode('utf-8')
    except:
        pass
#    json_string=json.dumps(info['body'])
    data = json.loads(data)
    del(data['Date'])
    del(data['WorldSeed'])
    del(data['Version'])
    del(data['MobileVersion'])
    del(data['BuildLabel'])
    del(data['Events'])
    del(data['Goals'])
    del(data['GlobalUpgrades'])
    del(data['FlashSales'])
    del(data['HubEvents'])
    del(data['NodeOverrides'])
    del(data['BadlandNodes'])
    del(data['PrimeAccessAvailability'])
    del(data['PrimeVaultAvailabilities'])
    del(data['LibraryInfo'])
    del(data['PVPChallengeInstances'])
#    del(data['PersistentEnemies']) 小小黑活动
    del(data['PVPAlternativeModes'])
    del(data['PVPActiveTournaments'])
    del(data['ProjectPct'])
    del(data['ConstructionProjects'])
    del(data['TwitchPromos'])
    '''
    剩余八个参数：
    Time              > 时间
    Alerts            > 警报      *
    Sorties           > 突击      *
    SyndicateMissions > 集团任务
    ActiveMissions    > 裂隙      *
    Invasions         > 入侵
    VoidTraders       > 虚空商人   *
    DailyDeals        > 每日折扣
    '''
    Syndicate = {'ArbitersSyndicate':[],'CephalonSudaSyndicate':[],'NewLokaSyndicate':[],'PerrinSyndicate':[],'AssassinsSyndicate':[],'RedVeilSyndicate':[],'EventSyndicate':[],'SteelMeridianSyndicate':[],'QuillsSyndicate':[],'CetusSyndicate':[]}
    for element in data['SyndicateMissions']:
        try:
            Syndicate[element['Tag']].append(element)
        except:
            pass
    data['SyndicateMissions'] = Syndicate
    '''
    ArbitersSyndicate      > 均衡仲裁者
    CephalonSudaSyndicate  > 中枢苏达
    NewLokaSyndicate       > 新世间
    PerrinSyndicate        > 佩兰数列
    AssassinsSyndicate     > 
    RedVeilSyndicate       > 血色面纱
    EventSyndicate         > 
    SteelMeridianSyndicate > 钢铁防线
    QuillsSyndicate        > 夜羽
    CetusSyndicate         > 赏金
    '''
    global worldData
    global warList
    global lastAlerts
    global thisAlerts
    #存储上一次警报
    try:
        lastAlerts = worldData['Alerts'][:]
    except:
        lastAlerts = []
    #存储worldstate数据
    worldData = data
    print('update complate...')
    #存储本次警报
    thisAlerts = worldData['Alerts'][:]
    #try:
    for i in thisAlerts:
        for j in lastAlerts:
            if i['_id']['$oid'] == j['_id']['$oid']: 
                thisAlerts.remove(i)
    #except:
    #    pass
    try:
        for i in thisAlerts:
            if 'countedItems' in i['MissionInfo']['missionReward']:
                item = i['MissionInfo']['missionReward']['countedItems'][0]['ItemType'].split('/')
                try: 
                    item = worldDict[0][item[len(item)-1]]
                except:
                    item = item[len(item)-1]
            elif 'items' in i['MissionInfo']['missionReward']:
                item = i['MissionInfo']['missionReward']['items'][0].split('/')
                try: 
                    item = worldDict[0][item[len(item)-1]]
                except:
                    item = item[len(item)-1]
            else:
                item = '现金'
            for element in ('泥炭萃取物','狗蛋','库娃遗传密码','枪托','枪机','破坏者','亡魂','希芙','光环','反应堆','催化剂','裂罅','Forma') :
                if (element in item): warList.append(i)
    except:
        pass
    timerLoop(60, updateJson)



#开始循环
print('loading directionary...')
#wroldData[0]是中>英
#wroldData[1]是英>中
worldDict = loadDict()
worldData = {}
warList = []
lastAlerts = []
thisAlerts = []
updateJson()
Sorties()
