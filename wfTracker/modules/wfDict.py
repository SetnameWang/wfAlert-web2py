# -*- coding: utf-8 -*-
import os
import json

#载入词库
def loadDict(name):
    path = os.path.dirname(os.path.realpath(__file__))
    file = open(path + name, "r",encoding= 'utf-8')
    data = file.read()
    itemDirc = json.loads(data)
    file.close()
    return itemDirc

#zhTrans = loadDict('\zhTrans.json')
comTrans = loadDict('\\comTrans.json')
wmTrans = loadDict('\\wmTranslate.json')
nodes = loadDict('\\ExportRegions.json')

#地点名
#wfDict.nodes['SolNode107']['name']
#星球名
#wfDict.nodes['SolNode107']['systemName']
