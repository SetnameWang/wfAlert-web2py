function getwmData(){
    $.ajax({
        //请求方式
        type:"GET",
        //文件位置
        url:"/wfTracker/static/js/wm.enTrans.json",
        //返回数据格式为json,也可以是其他格式如
        dataType: "json",
        //请求成功后要执行的函数，拼接html
        success: function(data){
            //storage.setItem("json_data",JSON.stringify(json_data));
            wmList='';
            keyList = [];
            for (var name in data)
            {
                wmList = wmList + name + ',' + data[name] + '|';
                keyList.push(name);
            }
            localStorage.setItem('wmList',wmList);
            localStorage.setItem('keyList',keyList);
            localStorage.setItem('warframeMarketData','True');
        }
    });
}

function getwmTranslate(){
    $.ajax({
        //请求方式
        type:"GET",
        //文件位置
        url:"/wfTracker/static/js/wm.zhTrans.json",
        //返回数据格式为json,也可以是其他格式如
        dataType: "json",
        //请求成功后要执行的函数，拼接html
        success: function(data){
            //storage.setItem("json_data",JSON.stringify(json_data));
            wmList='';
            keyList = [];
            for (var name in data)
            {
                wmList = wmList + name + ',' + data[name] + '|';
                keyList.push(name);
            }
            wmList = localStorage.getItem('wmList') + '|' + wmList;
            localStorage.setItem('wmList',wmList);
            keyList = localStorage.getItem('keyList') + ',' + keyList;
            localStorage.setItem('keyList',keyList);
            localStorage.setItem('warframeMarketTranslate','True');
        }
    });
}
function decodeData(strStream){
    dictReturn = [];
    tempory = strStream.split('|');
    for (var i=0;i<tempory.length;i++)
    {
        tempory1 = tempory[i].split(',');
        dictReturn[tempory1[0]] = tempory1[1];
    }
    return dictReturn
}
function detectData(){
    if(localStorage.getItem('warframeMarketData')==null){
        localStorage.removeItem('wmList');
        getwmData();
        if(localStorage.getItem('warframeMarketTranslate')==null){
            getwmTranslate();
        }else{
            wmList = localStorage.getItem('transList');
        }
    }else{
        wmList = localStorage.getItem('wmList');
    }
    strWmList = localStorage.getItem('wmList');
    wmList = decodeData(strWmList);
    strWmList = '';
    return wmList
}
function search(){
    nameList = localStorage.getItem('keyList').split(',');
    itemList = [];
    key = document.getElementById("searchBar").value.toLowerCase();
    re = /\|\|\|/;
    for (var i=0;i<nameList.length;i++){
        tempory = nameList[i].toLowerCase().replace(key,'|||');
        if(re.exec(tempory)!=null){
            itemList.push(nameList[i])
        }
    }
    output='';
    for (var i=0;i<itemList.length;i++){
        output = output + "<li onClick=\"reqWm('" + wmList[itemList[i]] + "','" + itemList[i] + "')\">" + itemList[i] + '</li>'
    }
    document.getElementById("optionDiv").innerHTML = '<ul>' + output + '</ul>';
    if(itemList.length*30+10 > 310) divLength=310;
    else divLength = itemList.length*30+10;
    document.getElementById("optionDiv").style.height = divLength;
}
function getData(){
    nameUrl = wmList[document.getElementById("searchBar").value];
    url = '/wfTracker/wm/api?nameUrl=' + nameUrl;
    $.ajax({
        //请求方式
        type:"GET",
        //文件位置
        url: url,
        //返回数据格式为json,也可以是其他格式如
        dataType: "json",
        //请求成功后要执行的函数，拼接html
        success: function(data){
            document.getElementById("displayUl").innerHTML = '<tr><th>玩家ID</th><th>销售数量</th><th>价格</th><th></th></tr>'
            for (var i=0;i<data['list'].length;i++){
                document.getElementById("displayUl").innerHTML = document.getElementById("displayUl").innerHTML + '<tr><td>' + data['list'][i]['userName'] + '</td><td>' + data['list'][i]['quantity'] + '</td><td>' + data['list'][i]['platinum'] + '<img src="/wfTracker/static/img/Platinum.png" style="width: 12px;box-shadow: none;"></td><td>' + '<img src="/wfTracker/static/img/copyImg.jpg" style="width: 20px;box-shadow: none;" onClick=\"printData(' + "'" +document.getElementById("searchBar").value + "','" + data['list'][i]['userName'] + "','" + data['list'][i]['platinum'] + "')\"" + '></td></tr>';
                document.getElementById("loading").style.opacity = 0;
            }
        },
        error : function(textStatus){
            console.info('Fail');
            document.getElementById("loading").style.opacity = 0;
        },
    });
}
function printData(engName,userName,platinum){
    document.getElementById("display").style.display = 'block';
    document.getElementById("display").style.height = document.body.scrollHeight;
    document.getElementById("copyBar").value = '/w ' + userName + ' Hi! I want to buy: [' + engName + '] for [' + platinum + '] platinum. (warframe.market&wf.setname.tk)';
    margin = document.body.scrollTop + (document.body.clientHeight - 50) / 2;
    document.getElementById("copyBar").style.margin = margin.toString() + ' 0 0 20%';
    document.getElementById("copyBar").focus();
    document.getElementById("copyBar").select();
}
function closeDisplay(){
    document.getElementById("display").style.display = 'none';
}
function reqWm(nameUrl, name){
    document.getElementById("searchBar").value = name;
    document.getElementById("loading").style.opacity = 1;
    getData();
}
wmList = detectData();
