import requests
from bs4 import BeautifulSoup
import re
import json
import os

last_launchpool_articles = {}

def save_articles_to_file(articles, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

def load_articles_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def binance_launchpool():

    url = 'https://www.binance.com/zh-TC/support/announcement/%E6%95%B8%E5%AD%97%E8%B2%A8%E5%B9%A3%E5%8F%8A%E4%BA%A4%E6%98%93%E5%B0%8D%E4%B8%8A%E6%96%B0?c=48&navId=48&hl=zh-TC'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
    }

    # 發起GET請求
    response = requests.get(url, headers=headers)

    # 檢查請求是否成功
    if response.status_code != 200:
        print(f"請求失敗，狀態碼: {response.status_code}")
        return

    # 使用 BeautifulSoup 解析 HTML 內容
    soup = BeautifulSoup(response.content, 'html.parser')

    # 將soup對象轉換成字符串
    soup_str = str(soup)

    # 使用正則表達式查找所有的JSON物件
    pattern = re.compile(r'{"id":\d+,"code":"\w+","title":"幣安*?新幣挖礦.*?","type":\d+,"releaseDate":\d+}')
    matches = pattern.findall(soup_str)

    # 將所有匹配的JSON字符串轉換成Python對象並放入列表中
    announcements = [json.loads(match) for match in matches]
    # 構造結果字典
    result_dict = {}
    for announcement in announcements:
        title = announcement['title']
        code = announcement['code']
        sanitized_title = title.replace(' ', '-').replace('，', '-').replace('、', '-').replace('(', '').replace(')', '')
        link = f"https://www.binance.com/zh-TC/support/announcement/{sanitized_title}-{code}"
        result_dict[title] = link

    # 順序反轉
    reversed_result_dict = dict(reversed(list(result_dict.items())))
    print(reversed_result_dict)
    return reversed_result_dict

def send_to_discord(webhook_url, message):
    data = {
        "content": message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("消息已成功發送到Discord")
    else:
        print(f"發送到Discord失敗，狀態碼: {response.status_code}")

def main():
    global last_launchpool_articles

    # Discord Webhook URL
    webhook_url = "Discord Webhook URL"

    last_launchpool_articles = load_articles_from_file('last_binance_articles.txt')

    now_launchpool_articles = binance_launchpool()

    # 比較兩個字典，找出新增的文章
    new_articles = {k: v for k, v in now_launchpool_articles.items() if k not in last_launchpool_articles}

    # 如果有新的文章，發送到Discord
    for title, url in new_articles.items():
        message = f"[📢]({url})  {title}\n[⛓️ 點擊查看]({url})"
        send_to_discord(webhook_url, message)

    # 更新last_launchpool_articles並保存到文件
    last_launchpool_articles = now_launchpool_articles
    save_articles_to_file(last_launchpool_articles, 'last_binance_articles.txt')

if __name__ == "__main__":
    main()
