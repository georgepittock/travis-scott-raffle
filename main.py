import random
import threading
import time
import re

import requests
import names

HEADERS = {
    "authority": "f1eb5xittl.execute-api.us-east-1.amazonaws.com",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="92"',
    "accept": "application/json, text/plain, */*",
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.108 Safari/537.36",
    "dnt": "1",
    "origin": "https://shop.travisscott.com",
    "sec-fetch-site": "cross-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://shop.travisscott.com/",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    }
SIZES = ['4', '4.5', '5', '5.5', '6', '6.5', '7', '7.5', '8', '8.5', '9', '9.5', '10', '10.5', '11', '11.5', '12',
         '12.5', '13', '14', '15']


def random_proxy():
    proxy_lines = open("proxies.txt").readlines()
    if len(proxy_lines) == 0:
        return None
    random_line = random.choice(proxy_lines).strip()
    if len(random_line.split(":")) == 2:
        return {
            "http": "http://{}".format(random_line),
            "https": "http://{}".format(random_line),
            }
    elif len(random_line.split(":")) == 4:
        splitted = random_line.split(":")
        return {
            "http": "http://{0}:{1}@{2}:{3}".format(
                splitted[2], splitted[3], splitted[0], splitted[1]
                ),
            "https": "http://{0}:{1}@{2}:{3}".format(
                splitted[2], splitted[3], splitted[0], splitted[1]
                ),
            }
    return None


def parse_product_id(url):
    headers = {
        'authority': 'shop.travisscott.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.108 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'dnt': '1',
        }
    headers = HEADERS | headers
    response = requests.get(url, headers=headers)
    return re.findall('"parent_id":(\d+)', response.text)[0]


def submit(pid):
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    email = random.choice(
        [
            first_name + last_name + str(random.randint(0, 999)) + "@" + catchall,
            first_name + str(random.randint(0, 999)) + last_name + str(random.randint(0, 999)) + "@" + catchall,
            first_name + str(random.randint(0, 999)) + last_name + str(random.randint(0, 999)) + "@" + catchall,
            first_name + last_name + "@" + catchall,
            last_name + first_name + "@" + catchall,
            first_name + "." + last_name + str(random.randint(0, 999)) + "@" + catchall,
            first_name + "." + str(random.randint(0, 999)) + last_name + str(random.randint(0, 999)) + "@" + catchall,
            first_name + "." + str(random.randint(0, 999)) + last_name + str(random.randint(0, 999)) + "@" + catchall,
            first_name + "." + last_name + "@" + catchall,
            last_name + "." + first_name + "@" + catchall,
            ]
        )

    size = random.choice(SIZES)
    params = (
        ("a", "m"),
        ("email", email),
        ("first", first_name),
        ("last", last_name),
        ("zip", postcode),
        ("telephone", str(random.randint(10000000000, 99999999999))),
        ("product_id", pid),
        ("kind", "shoe"),
        ("size", size),
        )
    while True:
        try:
            response = requests.get(
                "https://f1eb5xittl.execute-api.us-east-1.amazonaws.com/fragment/submit",
                headers=HEADERS,
                params=params,
                proxies=random_proxy(),
                )
            if response.ok and response.json() == {"msg": "thanks"}:
                print("Success")
            else:
                print(f"Failed {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error {e}")


if __name__ == "__main__":
    catchall = input("Enter your catchall @...: ")
    postcode = input("Enter your postcode: ")

    product_id = parse_product_id("https://shop.travisscott.com/")

    thread_count = int(input("How many threads: "))
    threads = [threading.Thread(target=submit, args=(product_id,)) for _ in range(thread_count)]
    for t in threads:
        t.start()
        time.sleep(0.5)
