from urllib.parse import parse_qs, urlparse

import requests

from config import cookies, headers
from tools import extract_surl_from_url, get_formatted_size

session = requests.Session()

session.cookies.update(cookies)

session.headers.update(headers)


def find_between(data, first, last):
    try:
        start = data.index(first) + len(first)
        end = data.index(last, start)
        return data[start:end]
    except ValueError:
        return None


def get_data(url: str):
    a = session.get(url, headers=headers, cookies=cookies)
    logid = find_between(a.text, "dp-logid=", "&")
    jstoken = (
        find_between(a.text, "window.jsToken%20%3D%20a%7D%3Bfn%28%22", "%22%29"),
    )
    shorturl = extract_surl_from_url(a.url)
    if not shorturl:
        return False
    params = (
        ("app_id", "250528"),
        ("web", "1"),
        ("channel", "dubox"),
        ("clienttype", "0"),
        (
            "jsToken",
            jstoken,
        ),
        ("dp-logid", logid),
        ("page", "1"),
        ("num", "20"),
        ("by", "name"),
        ("order", "asc"),
        ("site_referer", a.url),
        ("shorturl", shorturl),
        ("root", "1,"),
    )

    response = session.get("https://www.terabox.app/share/list", params=params)
    if not response.status_code == 200:
        return False
    r_j = response.json()
    if r_j["errno"]:
        return False
    if not "list" in r_j and not r_j["list"]:
        return False
    data = {
        "file_name": r_j["list"][0]["server_filename"],
        "link": r_j["list"][0]["dlink"],
        "thumb": r_j["list"][0]["thumbs"]["url3"],
        "size": get_formatted_size(int(r_j["list"][0]["size"])),
        "sizebytes": int(r_j["list"][0]["size"]),
    }
    return data


import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_driver_path = (
    "chromedriver.exe"  # download and place webdriver of chrome in the root directory
)
profile_name = "Default"
user_data_dir = "C:\\Users\\R0ld3\\AppData\\Local\\Google\\Chrome Beta\\User Data"  # do chrome://version in chrome to get
chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument(f"--profile-directory={profile_name}")
chrome_options.binary_location = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"  # do chrome://version in chrome to get
chrome_options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": os.getcwd(),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False,
    },
)

driver = webdriver.Chrome(keep_alive=chrome_driver_path, options=chrome_options)


def init_download(link):
    driver.get(link)
