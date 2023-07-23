import requests
import time
import json


def send(phone):
    print('token:', token)
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
        response_data = ret.json()
        print('response_data:', response_data)
    except Exception as e:
        print('send e:', e)


if __name__ == '__main__':
    global token, userid
    userid = input('输入Userid (回车直接跳过, 使用默认A-fa7a5900): ')
    token = input('先登录系统, 获取token后粘贴到这里后敲回车: ')

    with open('phones.txt', 'rb') as phonesFile:
        for pn in phonesFile.readlines():
            print('pn:', pn.strip().decode())
            phone = pn.strip().decode()
            send(phone)