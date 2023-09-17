import requests
from bs4 import BeautifulSoup
import json

def telegram_send_message(message, chat_id):
    bot_token = "blaw blaw blaw"
    telegram_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {'chat_id': chat_id, 'text': message}
    response = requests.post(telegram_url, data=params)

def delete_string_from_file(file_path, string_to_delete):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

        modified_content = file_content.replace(string_to_delete, '')

        with open(file_path, 'w') as file:
            file.write(modified_content)
    except:
        pass

def append_to_file(file_path, data_to_append):
    try:
        with open(file_path, 'a') as file:
            file.write(str(data_to_append) + "\n")
    except:
        pass

def check_string_in_file(file_path, target_string):
    try:
        with open(file_path, 'r') as file:
            if str(target_string) in file.read():
                return True
            return False
    except:
        pass

def get_chat_ids():
    with open("member.txt", 'r') as file:
        chat_ids = file.readlines()
    return chat_ids

def check_new_user():
    bot_token = "blaw blaw blaw"
    getUpdate = requests.get(f"https://api.telegram.org/bot{bot_token}/getUpdates").text
    datas = json.loads(getUpdate)

    for data in datas["result"]:
        try:
            status = data["my_chat_member"]["new_chat_member"]["status"]
            user_id = data["my_chat_member"]["from"]["id"]
            if status == "member" and not check_string_in_file("member.txt", user_id):
                append_to_file("member.txt", user_id)
            elif status == "kicked" and check_string_in_file("member.txt", user_id):
                delete_string_from_file("member.txt", user_id)
        except:
            pass
        try:
            user_id = data["message"]["from"]["id"]
            command = data["message"]["text"]
            if command == "/start" and not check_string_in_file("member.txt", user_id):
                append_to_file("member.txt", user_id)
            elif command == "/stop" and check_string_in_file("member.txt", user_id):
                delete_string_from_file("member.txt", user_id)
        except:
            pass

def check_news(news, website):
    req = requests.get(website)
    soup = BeautifulSoup(req.text, 'html.parser')
    links = soup.find_all('a')

    for link in links:
        link_text=str(link.text.strip())
        if "https" in link.get("href") and news in link_text.lower():
            if not check_string_in_file('sql.txt', link.get("href")):
                append_to_file('sql.txt', link.get("href"))
                chat_ids = get_chat_ids()
                for chat_id in chat_ids:
                    telegram_send_message(str(news +": " + link_text + "\n" + link.get("href")), chat_id)

news=['linux', ' cve ', ' cve-', 'exploit', 'vuln', 'windows', 'xss', 'csrf', 'ssrf', 'sql', 'iran', 'apt ']
websites=["https://news.ycombinator.com", "https://hckrnews.com"]
check_new_user()
for new in news:
    for website in websites:
        check_news(new, website)
        check_news(new, website)
