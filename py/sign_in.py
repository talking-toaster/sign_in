import json
import random
import time
import re
import os
from urllib.parse import urlencode
import requests
from requests.models import Response


def printy(s):
    print(f"\033[0;33;40m{s}\033[0m")


def delay(t: int = 1):
    time.sleep(random.random() + t)


class Signin:
    tiezi = []

    def __init__(self, user, password, host) -> None:
        self.user = user
        self.password = password
        self.session = requests.Session()
        self.host = host
        origin_headers = {
            'authority': self.host[8:],
            'sec-ch-ua':
            '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': self.host,
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': self.host,
            'accept-language':
            'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cookie': ""
        }
        try:
            with open(f"./{user}.cookie", "r") as f:
                origin_headers['cookie'] = f.read()
        except:
            printy("open file filed")
        self.session.headers.update(origin_headers)

    def login(self):
        data = {
            'username': self.user,
            'password': self.password,
            'ticket': '',
            'randstr': ''
        }
        login_url = self.host + '/wp-content/themes/LightSNS/module/action/login.php'
        response = self.session.post(login_url, data=data)
        #print(response.headers)
        try:
            cookie = re.findall(r'wordpress_logged_in_.*?;',
                                response.headers["Set-Cookie"])[0][:-1]
            self.session.headers.update({"cookie": cookie})
            with open(f'./{self.user}.cookie', 'w') as f:
                f.write(cookie)
        except:
            print("login===cookie error===>")
            print(response.headers)
        dic = json.loads(response.text)
        printy("login===ok===>")
        return 0 if dic["code"] == 1 else -1

    def publish(self):
        url = self.host + "/wp-content/themes/LightSNS/module/publish/bbs.php"
        data = {
            'title': '\u6253\u5361',
            'bbs_child_id': '0',
            'bbs_id': '5413',
            'content': '<p>\u6C34\u6C34\u6C34239<br/></p>',
            'topic': '\u6253\u5361',
            'ticket': '',
            'randstr': ''
        }
        '''
        self.session.headers.update({
            'referer':
            'https://www.utgamer.com/shuiku',
        })
        '''
        response = self.session.post(url=url, data=data)
        if (json.loads(response.text)['code'] == 1):
            printy("publish ok")
            return 0
        else:
            printy("publish error")
            printy(response.text)
            return -1

    def getlink(self):
        url = self.host
        response = self.session.get(url=url)
        link_raw = re.findall(r'<a class="post_list_link" href=".*?"',
                              response.text)
        link = []
        for l in link_raw:
            link.append(re.findall(r"\d+", l)[0])
        self.tiezi = link

    def comment(self, id):
        data = {
            'content': '666666',
            'post_id': str(id),
            'ticket': '',
            'randstr': ''
        }
        url = self.host + '/wp-content/themes/LightSNS/module/action/comment.php'
        response = self.session.post(url, data=data)
        if (json.loads(response.text)['code'] == 1):
            printy("comment ok")
            return 0
        else:
            printy(response.text)
            return -1

    def like(self, id):
        url = self.host + '/wp-content/themes/LightSNS/module/action/like-post.php'
        data = {
            'post_id': str(id),
        }
        response = self.session.post(url, data=data)
        if (json.loads(response.text)['code'] == 1):
            printy("like ok")
            return 0
        else:
            printy("like error")
            print(response.text)
            return -1

    def task_finish(self):
        url = self.host + '/wp-content/themes/LightSNS/module/action/task.php'
        finish = 0
        for i in range(10):
            data = {'task_id': 'task' + str(i), 'type': 'day'}
            response = self.session.post(url, data=data)
            if (json.loads(response.text)['code'] == 1):
                printy(f"task" + str(finish) + "finished")
                finish += 1
            else:
                print("task" + str(finish) + "unfinished")
                #printy(response.text)
                print(data)
            delay()
        return finish

    def sign(self):
        url = self.host + '/wp-content/themes/LightSNS/module/action/sign.php'
        data = {'sign': '1', 'ticket': '', 'randstr': ''}
        response = self.session.post(url, data=data)
        if (json.loads(response.text)['code'] == 1):
            printy("sign ok")
            return 0
        else:
            printy("sign error")
            print(response.text)
            return -1

    def test(self):
        print("test===session===>" + self.session.headers)

    def run(self):
        try:
            if (self.publish() == -1):
                print("run======>cookie timeout")
                delay()
                self.login()
                delay()
                self.publish()
            else:
                print("run=======>cookie ok")
        except:
            delay()
            self.login()
        delay()
        self.getlink()
        delay()
        comment = 0
        like = 0
        for l in self.tiezi:
            if comment < 1:
                if (self.comment(l) == 0):
                    comment += 1
                    delay()
            if like < 3:
                if (self.like(l) == 0):
                    like += 1
                    delay()
        printy("comment  " + str(comment) + "  like  " + str(like))
        delay()
        finish = self.task_finish()
        delay()
        coin = (finish + 1) * 50 if self.sign() == 0 else finish * 50
        printy("获取了 " + str(coin) + ' 金币')


def main():
    host = os.getenv('host')
    u = os.getenv('user')
    p = os.getenv('password')
    for i in range(len(u.split(','))):
        print("111")
        for h in host.split('.'):
            printy(h)
        user = u.split(',')[i]
        password = p.split(',')[i]
        printy(user)

        s = Signin(user, password, host)
        s.run()
        delay(5)


if __name__ == "__main__":
    main()
