import json
import time
from urllib.parse import urlparse, parse_qs

from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from .tagging_services import TAGGING_URLS

class TagValidator:
    def __init__(self, url: str, headless_mode: bool = False, disable_gpu: bool = False):
        chrome_options = Options()
        if headless_mode:
            chrome_options.add_argument("--headless=new")
        if disable_gpu:
            chrome_options.add_argument("--disable-gpu")
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.url = url
        self.tags_list = []

    def execute(self, *args):
        events = args
        try:
            self.driver.get(self.url)
            for event in events:
                event(self.driver)
        except Exception as e:
            print(e)
        self.tags_list += self.get_tags()

    def get_tags(self):
        tags_list = []
        for request in self.driver.requests:
            for header_url in TAGGING_URLS.keys():
                if header_url in request.url:
                    tags_list.append(TAGGING_URLS[header_url](request))
        return tags_list

    def to_json(self, file_name):
        with open(file_name, "w") as f:
            json.dump(self.tags_list, f, indent = 2)