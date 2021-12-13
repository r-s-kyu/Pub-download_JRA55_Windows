
# %%
import json
import re
from checkChromeVersion import checkChromeDriverVersion
import checkChromeVersion 
import importlib

importlib.reload(checkChromeVersion)

def ChromeVersionChecker():
    chromedriverVersion = f'./driver/chromedriverVersion.json'
    json_open = open(chromedriverVersion)
    chrome = json.load(json_open)
    chromeversion = chrome["chromedriver"]["Version"]

    driverVerion = checkChromeDriverVersion()

    if driverVerion == chromeversion[:len(driverVerion)]:
        checker = True
    else:
        checker = False
    return checker

def main():
    print(ChromeVersionChecker())

if __name__ == '__main__':
    main()
    