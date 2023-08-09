import os
import requests
import time
import json
import csv
import asyncio


async def getUser(phone):
    ts = int(round(time.time() * 1000))
    url = 'https://admin.edujia.com/admin/wmim/user/qryList.do?ts=%d' % ts
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json,text/javascript,*/*;q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Content-Length': '36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'token': token,
        'Userid': 'A-fa7a5900' if userid == '' else userid
    }
    data = {
        'page': 1,
        'pageSize': 50,
        'phone': phone
    }
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('url:', url)
    print('headers:', headers)
    print('data:', json.dumps(data))
    try:
        ret = requests.post(url=url, headers=headers, data=json.dumps(data))
        print('ret:', ret)
        response_data = ret.json()
        print('response_data:', response_data)
        if response_data.get('code') == '200':
            rlist = response_data.get('data').get('array')
            print('rlist:', rlist)
            return rlist
        else:
            return []
    except Exception as e:
        print('getUser e:', e)
        return []


def trans(dict):
    keys = ['phone', 'nickname', 'wxNickname', 'registerIp', 'createTime']
    res = []
    for key in keys:
        res.push(dict[key])
    return res


async def search():
    # 读取txt中电话号，逐行处理
    with open('phones.txt', 'rb') as phonesFile:
        for pn in phonesFile.readlines():
            phone = pn.strip().decode()
            print('phone:', phone)
            # 发送请求查询相关用户
            userList = await getUser(phone)
            # 以电话号为名创建csv文件
            fileName = '%s.csv' % phone
            isExists = os.path.exists(fileName)
            with open(fileName, mode='w' if not isExists else 'a', newline='') as file:
                writer = csv.writer(file)
                if (not isExists):
                    writer.writerow(['phone', 'nickname', 'wxNickname', 'registerIp', 'createTime'])
                for user in userList:
                    writer.writerow(trans(user))
            input('电话%s查询完成，发现%d个用户，回车继续' % (phone, len(userList)))


if __name__ == '__main__':
    global token, userid
    userid = input('输入Userid (回车直接跳过, 使用默认A-fa7a5900): ')
    token = input('先登录系统, 获取token后粘贴到这里后敲回车: ')
    print('userid:', 'A-fa7a5900' if userid == '' else userid)
    print('token:', token)
    asyncio.run(search())