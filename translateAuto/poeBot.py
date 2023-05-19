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

last = 0
timeoutTimes = 0


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


def __findEndTips(d):
    scrollJS = "document.getElementsByClassName('PageWithSidebarLayout_scrollSection__IRP9Y')[0].scrollTop = 0"
    d.execute_script(scrollJS)
    return d.find_element(By.XPATH, "//div[@class='ChatMessagesView_messagePair__CsQMW'][last()]/section[@class='ChatMessageFeedbackButtons_feedbackButtonsContainer__0Xd3I']")


async def translate(str = None):
    global last, timeoutTimes, driver
    '''
    每10秒一次请求, 避免过快
    '''
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
    inputArea = driver.find_element(By.CLASS_NAME, "ChatMessageInputView_textInput__Aervw")
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
            copyBtn = driver.find_element(By.XPATH, "//div[@class='ChatMessagesView_messagePair__CsQMW'][last()]/div[@class='ChatMessage_messageRow__7yIr2'][2]//*[@class='Button_buttonBase__0QP_m Button_flat__1hj0f MarkdownCodeBlock_copyButton__nm6Dw']")
            # print('copyBtn:', copyBtn)
            copyBtn.click()
            time.sleep(1)
            d = __getClipboard()
            print('===== Result: =====')
            print(d)
            return d
        except:
            print('Copy Fail')
            return await translate("不对，翻译的结果要用代码块")
    except:
        '''
        翻译的bot用一段时间会出现频繁超时的情况, 如果超时3次则关闭浏览器重新打开一个
        '''
        if timeoutTimes > 2:
            print('Reconnect bot ......')
            timeoutTimes = 0
            driver.close()
            driver = webdriver.Chrome(options = options)
            await getLightDBDocBoy()
            scrollJS = "document.getElementsByClassName('PageWithSidebarLayout_scrollSection__IRP9Y')[0].scrollTop = 0"
            driver.execute_script(scrollJS)
            return await translate()
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
    driver.get("https://poe.com/LightDBDocBoy")
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
        driver.get("https://poe.com/LightDBDocBoy")
        # 触发清除按钮
        driver.find_element(By.CLASS_NAME, "ChatMessageInputView_paintbrushWraper__DHMNW").click()
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
