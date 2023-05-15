import sys
import json
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


async def translate(str = None):
    inputArea = driver.find_element(By.CLASS_NAME, "ChatMessageInputView_textInput__Aervw")
    inputArea.clear()
    print('translate source: ')
    print(__getClipboard())
    if str == None:
        inputArea.send_keys(Keys.CONTROL, "V", Keys.ENTER)
    else:
        inputArea.send_keys(str, Keys.ENTER)
    try:
        endTipBtns = WebDriverWait(driver, timeout=60, poll_frequency=1).until(lambda d: d.find_element(By.XPATH, "//div[@class='ChatMessagesView_messagePair__CsQMW'][last()]/section[@class='ChatMessageFeedbackButtons_feedbackButtonsContainer__0Xd3I']"))
        try:
            copyBtn = driver.find_element(By.XPATH, "//div[@class='ChatMessagesView_messagePair__CsQMW'][last()]//*[@class='Button_buttonBase__0QP_m Button_flat__1hj0f MarkdownCodeBlock_copyButton__nm6Dw']")
            copyBtn.click()
            driver.implicitly_wait(1)
            d = __getClipboard()
            print('translate result: ')
            print(d)
            return d
        except:
            return await translate("不对，翻译的结果要用代码块")
    except:
        return await translate()


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
