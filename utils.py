import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# for gossip_finder
import requests
from bs4 import BeautifulSoup



channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "RGnfDCRGLy9hqZxWvMQ34bGdSSFVw1tM74Dto4Bmko0Gu8vIZAcChpVtprCgH2nOSwBblABZn/q1LkfJ5xw7EMyybQ8l7ndtWOqJvej/Bda2erNu/8wAM5uy5++pevybOeEUDaius0pAfheWkJFTCQdB04t89/1O/w1cDnyilFU=")


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(str(channel_access_token))
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""

def gossip_finder(count, keyword, nPush):
    payload = {
        'from':'/bbs/Gossiping/index.html',
        'yes':'yes'
    }

    requests.packages.urllib3.disable_warnings()    # no warning for not verifying
    rs = requests.session()
    res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=payload)
    res = rs.get('https://www.ptt.cc/bbs/Gossiping/index.html', verify=False)
    soup = BeautifulSoup(res.text, features="html.parser")
    done = 0
    page_searched = 0
    Text = ""
    while done == 0:
        for entry in soup.select('.r-ent'):
            if keyword in entry.select('.title')[0].text:
                this_push = entry.select('.nrec')[0].text
                if this_push:  # 處理推文如果不是數字情況
                    try:
                        this_push = int(this_push)  # 數字
                    except ValueError:
                        if this_push == '爆':
                            this_push = 99
                        elif this_push == 'XX':
                            this_push = -99
                        elif this_push.startswith('X'):
                            this_push = -10 * int(this_push[1])
                        else:
                            this_push = 0
                else:
                    this_push = 0

                if nPush == 0 or (0 < nPush <= this_push) or (0 > nPush >= this_push):
                    npush_text = ('0' if this_push == 0 else entry.select('.nrec')[0].text)
                    Text += '標題: ' + entry.select('.title')[0].text.strip() + '\n日期: ' + entry.select('.date')[0].text + ' \n作者: ' + entry.select('.author')[0].text + ' \n推噓文: ' + npush_text
                    Text += "\n網址: " + 'https://www.ptt.cc' + entry.find_all('a', href=True)[0]['href'] + "\n"
                    count = count - 1
                    page_searched = page_searched + 1
                    if count == 0 or page_searched == 10000:
                        done = 1
                        break
                    Text += '\n'
                    break
        # 上一頁
        urlLastPage = 'https://www.ptt.cc' + soup.find('div',class_='btn-group btn-group-paging').find_all('a')[1]['href']
        res = rs.get(urlLastPage)
        soup = BeautifulSoup(res.text, features="html.parser")

    if Text == "":
        Text = "查無資料"
    return Text