import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta


import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs


from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import logging
from aiogram import Bot, Dispatcher, executor, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler


API_TOKEN = "1085098338:AAEeedCzbyR1Nxnu4FhPGUD5llbJdlRRzGM"
URL_01 = "https://belgorod.nix.ru/autocatalog/usb_flash_drive_samsung/Samsung-MUF-64BE3-APC-CN-USB31-Flash-Drive-64Gb-RTL_352546.html"
URL_02 = "https://www.dns-shop.ru/product/52e32e60484c3330/pamat-usb-flash-32-gb-samsung-bar-plus-muf-32be3apc/"
URL_03 = "https://aliexpress.ru/item/1110652192.html?sku_id=12000028613434354&spm=a2g2w.productlist.search_results.0.36cf4aa62FIKPJ"
user_id = "649548096"


ua = UserAgent()
headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": ua.chrome
    }

options = webdriver.ChromeOptions()

web_driver_options.add_argument('headless')
web_driver_options.add_argument('--no-sandbox')
web_driver_options.add_argument('--disable-dev-shm-usage')
web_driver_options.add_argument("--disable-gpu")
web_driver_options.add_argument("--window-size=1920,1200")
web_driver_options.add_argument("--ignore-certificate-errors")
web_driver_options.add_argument("--disable-extensions")



def parser_nix(url):
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    cost = soup.find_all("a", class_ = "add_to_cart btn btn-t-0 btn-c-6 CanBeSold")
    unsorted_cost = [c.text for c in cost]
    sorted_cost = [string.replace('купить за ', ' ') for string in unsorted_cost]
    #return [string.replace('\xa0', ' ') for string in sorted_cost]
    return [string.replace('\xa0', ' ') for string in sorted_cost]


def parser_dns(url):
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    #cost = soup.find_all("div", class_ = "product-buy__price").text
    return soup.find_all("div", class_ = "product-buy__price")


def parser_ali(url):
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver: 
        driver.get(url) 
        cost = driver.find_element(By.XPATH, "//div[contains(@class, 'snow-price_SnowPrice__mainS__18x8np')]").text
    return cost


def auth(func):

    async def wrapper(message):
        if message['from']['id'] != 649548095:
            return await message.reply("Access denied", reply=False)
        return await func(message)
    return wrapper


#@auth
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

async def spam(bot: Bot):
    list_of_cost_nix = parser_nix(URL_01)
    list_of_cost_dns = parser_dns(URL_02)
    list_of_cost_ali = parser_ali(URL_03)

    await bot.send_message(649548096, f"=====================[BEGIN]=====================")
    await bot.send_message(649548096, f"Статистика по Никс [Samsung BAR PLUS 64GB]: {list_of_cost_nix}")
    await bot.send_message(649548096, f"Статистика по ДНС [Samsung BAR PLUS 32GB]: {list_of_cost_dns}")
    await bot.send_message(649548096, f"Статистика по Али [Alctron MC410]: {list_of_cost_ali}")
    await bot.send_message(649548096, f"=====================[END]=======================")

scheduler.add_job(spam, trigger='interval', seconds=120, kwargs={'bot': bot})
scheduler.start()



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
