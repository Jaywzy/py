import sys
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import win32clipboard as w
import win32con


options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)  # 不自动关闭浏览器
# options.add_argument('--start-maximized')       # 浏览器窗口最大化
driver = webdriver.Chrome(options = options)
BOT_URL = "https://poe.com/LightDBDocBoy"
last = 0
timeoutTimes = 0
copyFailTimes = 0


def setClipboard(data):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, data)
    w.CloseClipboard()


def __getClipboard():
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return d


def __getClipboardAsResult():
    res = __getClipboard()
    print('======== Result: ========')
    print(res)
    return res


def __scrollBottom():
    scrollJS = "document.getElementsByClassName('PageWithSidebarLayout_scrollSection__IRP9Y')[0].scrollTop = 0"
    driver.execute_script(scrollJS)


def __findEndTips(d):
    __scrollBottom()
    return d.find_element(By.XPATH, "//body/div/div/div/section/div[2]/div/div/div/div[last()]/section[1]")


async def __reconnectBot():
    global driver
    print('Reconnect bot ......')
    driver.close()
    driver = webdriver.Chrome(options = options)
    await getLightDBDocBoy()
    __scrollBottom()
    return await translate()


async def __resolveError(errMsg):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("翻译结果异常[%s]，请选择处理：" % errMsg)
    print("   r    --> 重启浏览器，重新连接")
    print("   m    --> 手动提供翻译结果，选择后直接使用剪切板内容作为结果")
    print("   b    --> 让bot用代码块")
    print(" 其他值 --> 重新发送文本继续翻译")
    opt = input('你的选择：')
    if opt == 'r':
        return await __reconnectBot()
    elif opt == 'm':
        return __getClipboardAsResult()
    elif opt == 'b':
        return await translate("用代码块")
    else:
        return await translate()


async def translate(str = None):
    global last, timeoutTimes, copyFailTimes
    '''
    每10秒一次请求, 避免过快
    now = int(time.time())
    if last == 0:
        last = now
    else:
        spend = now - last
        if spend < 10:
            print('last spend:', spend, 's, wait', 10 - spend, 's')
            time.sleep(10 - spend)
        else:
            print('last spend:', spend, 's, wait 3 s')
            time.sleep(3)
        last = int(time.time())
    '''
    time.sleep(2)
    inputArea = driver.find_element(By.XPATH, "//footer/div/div//textarea")
    inputArea.clear()
    print('-------------------- Source: --------------------')
    try:
        print(__getClipboard())
    except:
        pass
    if str == None:
        ''' 代码块形式提交原文 '''
        inputArea.send_keys("```", Keys.SHIFT, Keys.ENTER, Keys.CONTROL, "V", Keys.SHIFT, Keys.ENTER, "```", Keys.ENTER)
    else:
        inputArea.send_keys(str, Keys.ENTER)
    try:
        '''
        等待标志回答完毕的Tips条出现, 
        若未出现则可能超时或send fail, 那么except中重新再发一次
        '''
        WebDriverWait(driver, timeout=60, poll_frequency=2).until(__findEndTips)
        # print('__findEndTips: True')
        try:
            copyBtn = driver.find_element(By.XPATH, "//body/div/div/div/section/div[2]/div/div/div/div[last()]/div[2]//button[text()=' Copy']")
            # print('copyBtn:', copyBtn)
            copyBtn.click()
            time.sleep(1)
            res = __getClipboardAsResult()
            copyFailTimes = 0
            return res
        except:
            print('Copy Fail')
            copyFailTimes += 1
            '''
            有的模型总是不返回代码块, 如果累计超过3次则手动处理异常(暂停教育一下bot)
            '''
            if (copyFailTimes > 2):
                res = await __resolveError('缺失代码块')
                copyFailTimes = 0
                return res
            else:
                return await translate("不对，翻译的结果要用代码块")
    except:
        '''
        翻译的bot用一段时间会出现频繁超时的情况, 如果超时3次则手动处理异常
        '''
        if timeoutTimes > 2:
            res = await __resolveError('超时')
            timeoutTimes = 0
            return res
        else:
            timeoutTimes += 1
        print('__findEndTips: False')
        return await translate()


'''
打开bot网址, 设置cookie自动登录
可使用该方法保存cookies文件: 
    解开最底下两行注释, 然后运行本py文件时增加一个参数'login',
    打开bot网址后看到提示, 需要手动登录, 登录完成后输入任意键退出即可
'''
async def getLightDBDocBoy():
    driver.get(BOT_URL)
    print('sys.argv: ', sys.argv)
    if len(sys.argv) == 1 or len(sys.argv) == 4:
        with open('cookies.txt', 'r', encoding='utf8') as f:
            listCookies = json.loads(f.read())
        for cookie in listCookies:
            cookie_dict = {
                'domain': 'poe.com',
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                "expires": '',
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False
            }
        driver.add_cookie(cookie_dict)
        driver.get(BOT_URL)
        # 触发清除按钮
        driver.find_element(By.XPATH, "//footer/div/button").click()
        print('LightDBDocBoy ready!')
    elif len(sys.argv) == 2 and sys.argv[1] == 'login':
        input("等待登录, 登录成功后输入任意内容保存cookies文件")
        dictCookies = driver.get_cookies()
        jsonCookies = json.dumps(dictCookies)
        with open('cookies.txt', 'w') as f:
            f.write(jsonCookies)
        print('cookies保存成功, 窗口自动关闭!')
        driver.close()
    # test code below
    # d = __getClipboard()
    # print('translate source: ', d)
    # translate()


# if __name__ == "__main__":
#     getLightDBDocBoy()
