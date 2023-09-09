import requests
from bs4 import BeautifulSoup

def telegram_send_message(message):
    bot_token = "blaw blaw blaw"
    chat_id = "blaw"
    telegram_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {'chat_id': chat_id, 'text': message}
    response = requests.post(telegram_url, data=params)

def save_link_to_file(link):
    with open('sql.txt', 'a') as file:
        file.write(link + '\n')

def check_link_in_file(link):
    with open('sql.txt', 'r') as file:
        if link in file.read():
            return True
        return False

def check_news(news, website):
    req = requests.get(website)
    soup = BeautifulSoup(req.text, 'html.parser')
    links = soup.find_all('a')

    for link in links:
        link_text=str(link.text.strip())
        if "https" in link.get("href") and news in link_text.lower():
            if not check_link_in_file(link.get("href")):
                save_link_to_file(link.get("href"))
                telegram_send_message(str(news +": " + link_text + "\n" + link.get("href")))

news=['linux', ' cve ', ' cve-', 'exploit', 'vuln', 'windows', 'xss', 'csrf', 'ssrf', 'sql', 'iran', 'apt ']
websites=["https://news.ycombinator.com", "https://hckrnews.com"]
for new in news:
    for website in websites:
        check_news(new, website)
        check_news(new, website)
