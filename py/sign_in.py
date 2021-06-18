import time
import requests
url = 'https://www.utgamer.com'
origin_headers = {
  'authority': 'www.utgamer.com',
  'sec-ch-ua':
  '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
  'accept': 'application/json, text/javascript, */*; q=0.01',
  'x-requested-with': 'XMLHttpRequest',
  'sec-ch-ua-mobile': '?0',
  'user-agent':
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48',
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'origin': 'https://www.utgamer.com',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://www.utgamer.com',
  'accept-language':
  'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
  'cookie': ""
  }
start = time.time()
response = requests.get(url,headers=origin_headers)
print(time.time()-start)
print(response.text)
