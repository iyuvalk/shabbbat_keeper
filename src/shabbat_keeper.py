#!/usr/local/bin/python3

import requests
from bottle import Bottle, get, response, run
import time
import datetime

# MODIIN = 282926
HEBCAL_URL = "https://www.hebcal.com/shabbat/?cfg=json&geo=geoname&geonameid="
LATEST_RESULT_CACHE = {}

def get_current_date():
    return str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)

def get_hebcal_raw_res(geonameid):
    if geonameid not in LATEST_RESULT_CACHE or LATEST_RESULT_CACHE[geonameid]["ts"] != get_current_date():
        LATEST_RESULT_CACHE[geonameid] = {
            "raw_data": requests.get(HEBCAL_URL + str(geonameid)).json(),
            "ts": get_current_date()
        }
    return LATEST_RESULT_CACHE[geonameid]["raw_data"]

def get_next_item_by_category(geonameid, category):
    raw_hebcal_info = get_hebcal_raw_res(geonameid)
    for item in raw_hebcal_info["items"]:
        if item["category"] == category:
            return item
    return None

def get_next_item_date_by_category(geonameid, category):
    item = get_next_item_by_category(geonameid, category)
    if item is not None:
        return datetime.datetime.fromisoformat(item["date"]).timestamp()
    return 0


@get("/next_candle_lighting_date/<geonameid:re:[0-9]{1,60}>")
def get_next_candle_lighting_date(geonameid):
    try:
        return str(get_next_item_date_by_category(geonameid, "candles"))
    except Exception as ex:
        print(ex)
        return "0"

@get("/next_havdalah_date/<geonameid:re:[0-9]{1,60}>")
def get_next_havdalah_date(geonameid):
    try:
        return str(get_next_item_date_by_category(geonameid, "havdalah"))
    except Exception as ex:
        print(ex)
        return "0"

@get("/next_parasha/<geonameid:re:[0-9]{1,60}>")
def get_next_parasha(geonameid):
    item = get_next_item_by_category(geonameid, "parashat")
    if item is not None:
        return str(item["title"])
    else:
        return "-"

@get("/seconds_till_next_candle_lighting_date/<geonameid:re:[0-9]{1,60}>")
def get_seconds_till_next_candle_lighting_date(geonameid):
    res = float(get_next_candle_lighting_date(geonameid)) - time.time()
    if res >= 0:
        return str(res)
    return "0"

@get("/seconds_till_next_havdalah_date/<geonameid:re:[0-9]{1,60}>")
def get_seconds_till_next_havdalah_date(geonameid):
    res = float(get_next_havdalah_date(geonameid)) - time.time()
    if res >= 0:
        return str(res)
    return "0"


run(host='0.0.0.0', port=80)