from pprint import pprint
import re
from bs4 import BeautifulSoup
import curl_cffi
import urllib.parse
import pandas as pd

BASE_URL = "https://www.adforum.com"

headers = {
    "referer": "https://www.adforum.com/directories/agency/advertising?location=city:Chicago&discipline_strkey=DSP010",
    "x-requested-with": "XMLHttpRequest",
}


def extract_email_from_script(script_text):
    m = re.search(r"unescape\(['\"](.*?)['\"]\)", script_text)
    if not m:
        return None
    encoded = m.group(1)
    decoded_html = urllib.parse.unquote(encoded)

    # 去掉 document.write(...)
    cleaned = re.sub(r"^document\.write\(|\);?$", "", decoded_html).strip("'\"")

    inner = BeautifulSoup(cleaned, "html.parser")
    return inner.text


with curl_cffi.Session() as s:
    paths = []
    page = 1
    while True:
        # sleep random
        import time
        import random

        time.sleep(random.uniform(5, 7))

        url = f"https://www.adforum.com/search/find/loadmore?location=city:Chicago&discipline_strkey=DSP010&e=agency&rtpl=ListEntities&l=25&o=&p={page}"
        resp = s.get(
            url,
            headers=headers,
            impersonate="chrome",  # 重点，让 curl_cffi 像 Chrome 一样发请求
        )
        resp = resp.json()
        status = resp["status"]
        if status == "noresults":
            break
        page += 1
        soup = BeautifulSoup(resp["html"], "lxml")
        els = soup(class_="b-search_result__link--title")
        for el in els:
            print(el.text)
            paths.append(el.get("href"))
    pprint(paths)
    res = []
    count = 0
    # new_paths = ["/agency/6718733/profile/9rooftops"]
    for path in paths:
        r = s.get(BASE_URL + path, headers=headers, impersonate="chrome")
        time.sleep(random.uniform(5, 7))
        soup = BeautifulSoup(r.text, "lxml")
        info = soup.find("div", class_="agency-basic-info")
        if not info:
            continue
        el = soup.find("h2", class_="af-company-title")
        agency = el.text.strip() if el else ""
        location = info.find("address")
        location = location.text.strip() if location else ""
        if location != "":
            clean = re.sub(r"\s+", " ", location).strip()
            location = clean
        website = info.find(class_="agency-info__text--alt")
        if website:
            website = website.find("a")
            if website:
                website = website.get("href") if website else ""
        contact = info.find(class_="fullname")
        contact = contact.text if contact else ""
        phone = info.find(itemprop="telephone")
        phone = phone.text.strip() if phone else ""
        script_el = info.find("script")
        if script_el:
            script_text = script_el.text
            email = extract_email_from_script(script_text)
        else:
            email = ""

        temp = {
            "agency": agency,
            "location": location,
            "website": website,
            "contact": contact,
            "phone": phone,
            "email": email,
        }
        res.append(temp)
        count += 1
        print(f"Successfully Scraping Count: {count}")
        for k, v in temp.items():
            print(f"{k}: {v}")
        print("-" * 20)
    # write to a csv

    df = pd.DataFrame(res)
    df.to_csv("adforum_agencies.csv", index=False)
