from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
from bs4 import BeautifulSoup
import sys
import csv
import os
import time
import logging
# import traceback


logging.basicConfig(
    filename='runninglog.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# 获取查看按钮，onclick属性中的url
def getButton(domian, zh):
    print('sessionid:', sessionid)
    url = 'http://%s/zjfx/jsp/ajxx/queryCx.action' % domian
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '204',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cookie': 'SHAREJSESSIONID=%s' % sessionid
    }
    request_body = MultipartEncoder(
        {
            'yhzh.zh': zh,
            'yhzh.kssj': '2023-08-16',
            'pageList.curPage': '1'
        }
    )
    headers['Content-Type']= request_body.content_type

    print('url:', url)
    print('headers:', headers)
    print('request_body:', request_body)

    try:
        ret = requests.post(url=url, headers=headers, data=request_body)
        soup = BeautifulSoup(ret.text, 'html.parser')
        # print('soup:', soup)
        btns = soup.find_all('button')
        flag = False
        for b in btns:
            # print('~~~~~~~~~~ b:')
            # print(b)
            str = b.string
            # print('~~~~~~~~~~ str:', str)
            if '查看' in str:
                flag = True
                try:
                    clickStr = b.get('onclick')
                    # print('~~~~~~~~~~ clickStr:', clickStr)
                    viewPageUrl = 'http://%s%s' % (domian, extract_quotes(clickStr))
                    # print('~~~~~~~~~~ viewPageUrl:', viewPageUrl)
                    getViewPage(viewPageUrl, zh)
                except Exception as e:
                    print('getViewPageUrls e:', e)
                break
        if not flag:
            list_not = []
            list_not.append(zh.strip() + '\t')
            with open('result_not_checked.csv', 'a', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(list_not)
                print('%s 该账号无法查看' % str(zh))
                logging.warning('【警告】 %s 该账号无法查看！！已记录在result_not_checked.csv' % zh)

    except Exception as e:
        print('getButton e:', e)
        logging.error('getButton 错误')


# 爬取详情页信息
def getViewPage(url, zh):
    try:
        cookies = {'SHAREJSESSIONID': sessionid}
        viewPage = requests.get(url, cookies=cookies)
        soup = BeautifulSoup(viewPage.text, 'html.parser')
        # print('~~~~~~~~~~~~~~~~ soup:', soup)
        tableEles = soup.find_all('table')
        # print('~~~~~~~~~~~~~~~~ tableEles:', tableEles)
        vals = []
        for tableEle in tableEles:
            trEles = tableEle.find_all('tr')
            for trEle in trEles:
                tdEles = trEle.find_all('td')
                for tdEle in tdEles:
                    val = tdEle.text
                    vals.append(val.strip() + '\t')
            break
        # print('~~~~~~~~~~~ vals:')
        # print(vals)
        columns = vals[0::2]
        # print('~~~~~~~~~~~ columns len:', len(columns))
        # print('~~~~~~~~~~~ columns:', columns)
        list = vals[1::2]
        # print('~~~~~~~~~~~ list len:', len(list))
        # print('~~~~~~~~~~~ list:', list)
        if os.path.exists('result.csv'):
            # print('result.csv 存在')
            with open('result.csv', 'a', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(list)
                print('%s 录入完成' % str(zh))
                logging.info('%s 录入完成' % str(zh))
        else:
            print('result.csv 不存在')
            with open('result.csv', 'a', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerow(list)
                print('%s 录入完成' % str(zh))
                logging.info('%s 录入完成' % str(zh))
    except Exception as e:
        print('getViewPage e:', e)
        logging.error('getViewPage 错误')


# 获取单引号中内容
def extract_quotes(text):
    start = text.index("'") + 1
    end = text.index("'", start)
    return text[start:end]


if __name__ == '__main__':
    global sessionid
    sessionid = input('先登录系统, 获取sessionid后粘贴到这里后敲回车: ')
    domian = input('输入ip: ')
    intervalTime = input('输入请求时间间隔（单位秒）：')

    try:
        with open('cards.txt', 'rb') as cardsFile:
            logging.info('读取卡号，开始录入~~')
            for yhzh in cardsFile.readlines():
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                # print('yhzh:', yhzh.strip().decode())
                zh = yhzh.strip().decode()
                getButton(domian, zh)
                time.sleep(int(intervalTime))
        input("全部完成，恭喜！！！")
        sys.exit()
    except Exception as e:
        print('main e:', e)
        logging.error('main 错误')
        # traceback.print_exc()
        input("Press any key to exit...")
        sys.exit()