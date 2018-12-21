# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request

from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template

app = Flask(__name__)

slack_token = 'xoxb-503049869125-506761050128-aAB2vuXTSuXtGXboCFUHVKyr'
slack_client_id = '503049869125.508549271159'
slack_client_secret = '0d4cff9f98dfeb71d37a5ca43395039f'
slack_verification = '7DurBb5fYeEnC2ZgDmJg3xaG'
sc = SlackClient(slack_token)

# 여러번 호출하는 증상 완화 코드 적용이 안됨
# if slack_event['event_time'] < (datetime.now() - timedelta(seconds=1)).timestamp():
#     return make_response("this message is before sent.", 200, {"X-Slack-No-Retry": 1})
# 크롤링 함수 구현하기
def _crawl_naver_keywords(text):
    # 여기에 함수를 구현해봅시다.
    #     url = "http://hiphople.com/news_kr"
    #     req = urllib.request.Request(url)

    #     #크롤링과정
    #     sourcecode = urllib.request.urlopen(url).read()
    #     soup = BeautifulSoup(sourcecode, "html.parser")
    #     keywords = []
###########################################################################################




    if "국내 뉴스" in text:
        url = "http://hiphople.com/news_kr"
        req = urllib.request.Request(url)

        # 크롤링과정
        sourcecode = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sourcecode, "html.parser")
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

        keywords = []
        list_href = []
        list_content = []
        final_keywords = []
        full_url = []
        full_ = []

        for href in soup.find_all("a", class_="ab-link"):
            list_href.append(href["href"])

        for i in range(0, len(list_href)):
            url = "http://hiphople.com/news_kr" + list_href[i]
            req = urllib.request.Request(url)
            sourcecode = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(sourcecode, "html.parser")

            for source in soup.find_all("h1", class_="ah-title"):
                list_content.append(source.get_text())

        for i in range(0, 10):
            full_ = "http://hiphople.com/news_kr" + list_href[i]
            full_url.append(full_)

        for i in range(0, 10):
            message = list_content[i] + full_url[i]
            final_keywords.append(message)

        return u'\n'.join(final_keywords)
    if "해외 뉴스" in text:
        url = "http://hiphople.com/news_world"
        req = urllib.request.Request(url)

        # 크롤링과정
        sourcecode = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sourcecode, "html.parser")
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

        keywords = []
        list_href = []
        list_content = []
        final_keywords = []
        full_url = []
        full_ = []

        for href in soup.find_all("a", class_="ab-link"):
            list_href.append(href["href"])

        for i in range(0, len(list_href)):
            url = "http://hiphople.com/news_kr" + list_href[i]
            req = urllib.request.Request(url)
            sourcecode = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(sourcecode, "html.parser")

            for source in soup.find_all("h1", class_="ah-title"):
                list_content.append(source.get_text())

        for i in range(0, 10):
            full_ = "http://hiphople.com/news_kr" + list_href[i]
            full_url.append(full_)

        for i in range(0, 10):
            message = list_content[i] + full_url[i]
            final_keywords.append(message)

        return u'\n'.join(final_keywords)


###########################################################################################
    if "주간 랩" in text :
        url = "http://hiphopplaya.com/g2/bbs/board.php?bo_table=openmic&r=ok"
        req = urllib.request.Request(url)
        #크롤링과정
        sourcecode = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sourcecode, "html.parser")
        keywords = []
        final_keywords = []
        #1~3위까지 뽑아서 keywords에 append

        for data in (soup.find_all("div", class_="op_row_col_subject float_left cut_str bold")) :
            if not data.get_text() in keywords :
                if len(keywords) >= 3:
                    break
                keywords.append(data.get_text().strip())

        #4~5위까지 뽑아서 keywords에 append
        for data in (soup.find_all("div", class_="op_row_col_subject float_left cut_str ")) :
            if not data.get_text() in keywords :
                if len(keywords) >= 5:
                    break
                keywords.append(data.get_text().strip())

        for i in range(0,5) :
            message = str(i+1) + '위. ' + keywords[i]
            final_keywords.append(message)

        return "★★★★★★★주간 언더 랩 TOP 5★★★★★★★\n\n"+ u'\n'.join(final_keywords)

    # 한글 지원을 위해 앞에 unicode u를 붙혀준다.
###########################################################################################
    if "공연 정보" in text :
        url = "https://hiphopplaya.com/g2/bbs/board.php?bo_table=calendar&r=ok "
        req = urllib.request.Request(url)

        sourcecode = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sourcecode, "html.parser")

        date_ = []
        yoil = []
        event_title = []
        final_keywords = []
        list_href = []
        message = []
        num = 15

#예매링크 연결 코드... 잘안됨
        # for href in soup.find_all("a", class_= "cal_subject_a"):
        #     list_href.append(href["href"])
        # print(list_href)
        #
        # for i in range(0, len(list_href)):
        #     full_ = "https://hiphopplaya.com" + list_href[i]
        #     full_url.append(full_)
        #
        # print(full_url)
        # for i in full_url:
        #     url = i
        #     sourcecode = urllib.request.urlopen(url).read()
        #     soup = BeautifulSoup(sourcecode, "html.parser")
        #     soup.find("div", id="view_link_content").find("a")["href"]

        for data in (soup.find_all("div", class_ = "cal_date eng bold help")) :
            if not data.get_text() in date_ :
                if len(date_) >= num:
                    break
                date_.append(data.get_text().strip())

        for data in (soup.find_all("div",  class_= "cal_yoil help han ")) :
            if len(yoil) >= num:
                break

            yoil.append(data.get_text().strip())

        for data in (soup.find_all("div", class_ = "cal_col2 float_left")) :
            if not data.get_text() in event_title :
                if len(event_title) >= num:
                    break
                event_title.append(data.get_text().strip())

        for i in range(0, num):
            message = date_[i] + "일 " + yoil[i] + "   " + event_title[i]
            final_keywords.append(message)




        return "★★★★★★★주간 공연정보★★★★★★★\n\n"+ u'\n'.join(final_keywords)

###########################################################################################
    else :
        return "국내 뉴스, 해외 뉴스, 공연 정보, 주간 랩 중에 고르세요.\n"
# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]

        keywords = _crawl_naver_keywords(text)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords
        )

        return make_response("App mention message has been sent", 200, )

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
